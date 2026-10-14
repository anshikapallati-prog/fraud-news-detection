"""
TruthLens AI — Authentication Module
Demo-grade local authentication: SQLite user store, PBKDF2 password hashing
(stdlib only), and JWT sessions.

Scope note: this is intentionally simple and suitable for a college project
demo running on the developer's own machine. It is NOT hardened for public,
multi-user production use (no rate limiting, no email verification, token in
browser localStorage). Do not present it as production-grade security.
"""

import hashlib
import hmac
import os
import secrets
import sqlite3
import time
from pathlib import Path

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from config import settings

JWT_ALGORITHM = "HS256"
TOKEN_LIFETIME_SECONDS = 7 * 24 * 60 * 60  # 7 days
PBKDF2_ITERATIONS = 200_000

bearer_scheme = HTTPBearer(auto_error=False)


def get_db_path() -> Path:
    """Database location. Overridable via AUTH_DB_PATH (used by tests)."""
    return Path(os.getenv("AUTH_DB_PATH", Path(__file__).parent / "users.db"))


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    return conn


def _secret() -> str:
    if not settings.SECRET_KEY:
        raise RuntimeError(
            "SECRET_KEY is not set. Add it to backend/.env (see .env.example)."
        )
    return settings.SECRET_KEY


def hash_password(password: str) -> str:
    """Hash a password with a random salt. Returns 'salt_hex$hash_hex'."""
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS
    )
    return f"{salt.hex()}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    """Constant-time password check. Never reveals which part mismatched."""
    try:
        salt_hex, hash_hex = stored.split("$", 1)
        expected = bytes.fromhex(hash_hex)
    except (ValueError, TypeError):
        return False
    candidate = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), bytes.fromhex(salt_hex), PBKDF2_ITERATIONS
    )
    return hmac.compare_digest(candidate, expected)


class EmailAlreadyRegistered(ValueError):
    """Raised when registering an email address that already exists."""


def normalize_email(email: str) -> str:
    return email.strip().lower()


def create_user(email: str, password: str) -> dict:
    """Create a user. Raises EmailAlreadyRegistered on duplicates."""
    email = normalize_email(email)
    conn = _connect()
    try:
        created_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        try:
            cursor = conn.execute(
                "INSERT INTO users (email, password_hash, created_at) VALUES (?, ?, ?)",
                (email, hash_password(password), created_at),
            )
        except sqlite3.IntegrityError:
            raise EmailAlreadyRegistered(email)
        conn.commit()
        return {"id": cursor.lastrowid, "email": email, "created_at": created_at}
    finally:
        conn.close()


def authenticate_user(email: str, password: str) -> dict | None:
    """Return the public user dict when credentials are valid, else None."""
    email = normalize_email(email)
    conn = _connect()
    try:
        row = conn.execute(
            "SELECT id, email, password_hash, created_at FROM users WHERE email = ?",
            (email,),
        ).fetchone()
    finally:
        conn.close()
    if row is None:
        return None
    if not verify_password(password, row["password_hash"]):
        return None
    return {"id": row["id"], "email": row["email"], "created_at": row["created_at"]}


def create_token(user_id: int, email: str) -> str:
    """Create a signed JWT session token."""
    now = int(time.time())
    payload = {
        "sub": str(user_id),
        "email": email,
        "iat": now,
        "exp": now + TOKEN_LIFETIME_SECONDS,
    }
    return jwt.encode(payload, _secret(), algorithm=JWT_ALGORITHM)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> dict:
    """FastAPI dependency: resolve the Bearer token to a user or raise 401."""
    if credentials is None or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated. Please sign in.",
        )
    try:
        payload = jwt.decode(
            credentials.credentials, _secret(), algorithms=[JWT_ALGORITHM]
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired. Please sign in again.",
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session. Please sign in again.",
        )

    conn = _connect()
    try:
        row = conn.execute(
            "SELECT id, email, created_at FROM users WHERE id = ?",
            (payload.get("sub"),),
        ).fetchone()
    finally:
        conn.close()
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account no longer exists. Please register again.",
        )
    return {"id": row["id"], "email": row["email"], "created_at": row["created_at"]}
