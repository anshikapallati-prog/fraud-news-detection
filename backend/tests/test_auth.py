"""
TruthLens AI — Authentication Endpoint Tests
Uses a temporary SQLite file so the real users.db is never touched.
"""

import os
import tempfile

import pytest
from httpx import AsyncClient, ASGITransport

# Point auth at an isolated database BEFORE the app is imported.
_tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
_tmp.close()
os.environ["AUTH_DB_PATH"] = _tmp.name
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-pytest-only")

from main import app  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def _cleanup_test_db():
    """Remove the temporary test database when the session finishes."""
    yield
    try:
        os.unlink(_tmp.name)
    except OSError:
        pass


@pytest.mark.asyncio
async def test_register_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/auth/register",
            json={"email": "student@example.com", "password": "correct-horse-42"},
        )
    assert response.status_code == 201
    data = response.json()
    assert data["user"]["email"] == "student@example.com"
    assert "password" not in data["user"]
    assert data["token_type"] == "bearer"
    assert len(data["token"]) > 20


@pytest.mark.asyncio
async def test_register_duplicate():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post(
            "/api/auth/register",
            json={"email": "dupe@example.com", "password": "some-password-1"},
        )
        response = await client.post(
            "/api/auth/register",
            json={"email": "DUPE@example.com", "password": "other-password-2"},
        )
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_register_invalid_email():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/auth/register",
            json={"email": "not-an-email", "password": "some-password-1"},
        )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_short_password():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/auth/register",
            json={"email": "short@example.com", "password": "abc"},
        )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_success_and_me():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post(
            "/api/auth/register",
            json={"email": "login@example.com", "password": "my-secret-pw-9"},
        )
        login = await client.post(
            "/api/auth/login",
            json={"email": "login@example.com", "password": "my-secret-pw-9"},
        )
    assert login.status_code == 200
    token = login.json()["token"]

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        me = await client.get(
            "/api/auth/me", headers={"Authorization": f"Bearer {token}"}
        )
    assert me.status_code == 200
    assert me.json()["email"] == "login@example.com"


@pytest.mark.asyncio
async def test_login_wrong_password():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post(
            "/api/auth/register",
            json={"email": "victim@example.com", "password": "right-password-1"},
        )
        response = await client.post(
            "/api/auth/login",
            json={"email": "victim@example.com", "password": "wrong-password-2"},
        )
    assert response.status_code == 401
    # Must not reveal whether the email exists.
    assert "victim" not in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_me_without_token():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/auth/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_with_bad_token():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(
            "/api/auth/me", headers={"Authorization": "Bearer totally.invalid.token"}
        )
    assert response.status_code == 401
