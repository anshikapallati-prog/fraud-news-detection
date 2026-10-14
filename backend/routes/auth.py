"""
TruthLens AI — Authentication Routes
POST /api/auth/register, POST /api/auth/login, GET /api/auth/me.
"""

import re

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, field_validator

import auth as auth_service
from auth import EmailAlreadyRegistered, get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class RegisterRequest(BaseModel):
    """Create a new local account."""

    email: str = Field(..., min_length=3, max_length=254)
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if not EMAIL_PATTERN.match(value.strip()):
            raise ValueError("Enter a valid email address.")
        return value.strip()


class LoginRequest(BaseModel):
    """Sign in to an existing local account."""

    email: str = Field(..., min_length=3, max_length=254)
    password: str = Field(..., min_length=1, max_length=128)


class UserPublic(BaseModel):
    """Public user info — never includes a password hash."""

    id: int
    email: str
    created_at: str


class AuthResponse(BaseModel):
    """Returned by register and login: the user plus a session token."""

    user: UserPublic
    token: str
    token_type: str = "bearer"


@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new account",
)
async def register(request: RegisterRequest) -> AuthResponse:
    """Create a local account and return a session token (auto sign-in)."""
    try:
        user = auth_service.create_user(request.email, request.password)
    except EmailAlreadyRegistered:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists. Try signing in.",
        )
    token = auth_service.create_token(user["id"], user["email"])
    return AuthResponse(user=UserPublic(**user), token=token)


@router.post("/login", response_model=AuthResponse, summary="Sign in")
async def login(request: LoginRequest) -> AuthResponse:
    """Verify credentials and return a session token."""
    user = auth_service.authenticate_user(request.email, request.password)
    if user is None:
        # Deliberately vague: never reveal whether the email exists.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
        )
    token = auth_service.create_token(user["id"], user["email"])
    return AuthResponse(user=UserPublic(**user), token=token)


@router.get("/me", response_model=UserPublic, summary="Current account")
async def me(current_user: dict = Depends(get_current_user)) -> UserPublic:
    """Return the account belonging to the presented Bearer token."""
    return UserPublic(**current_user)
