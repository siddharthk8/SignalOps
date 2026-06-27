import pytest
from httpx import AsyncClient

from tests.conftest import auth_header, create_test_user, login_user


@pytest.mark.anyio
async def test_create_user_success(client: AsyncClient):
    response = await client.post(
        "/api/v1/users",
        json={
            "first_name": "first-name",
            "last_name": "last-name",
            "email": "test2@example.com",
            "password": "String123",
        },
    )

    assert response.status_code == 201
    data = response.json()

    assert data["email"] in "test2@example.com"
    assert "id" in data
    assert "password" not in data
    assert "password_hash" not in data


@pytest.mark.anyio
async def test_create_user_duplicate_email(client: AsyncClient):
    await create_test_user(client)

    response = await client.post(
        "/api/v1/users",
        json={
            "first_name": "first-name",
            "last_name": "last-name",
            "email": "test@example.com",
            "password": "String123",
        },
    )

    assert response.status_code == 400
    data = response.json()

    assert data["message"] == "User with this email already exists."


@pytest.mark.anyio
async def test_get_me_success(client: AsyncClient):
    user = await create_test_user(client)
    token = await login_user(client, user["id"])
    header = auth_header(token)

    response = await client.get("/api/v1/users/me", headers=header)

    assert response.status_code == 201
    data = response.json()

    assert data["email"] in "test@example.com"
    assert "id" in data
