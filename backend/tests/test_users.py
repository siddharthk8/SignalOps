import pytest
from httpx import AsyncClient

from tests.conftest import DEFAULT_USER, auth_header, create_test_user, login_user


@pytest.mark.anyio
async def test_create_user_success(client: AsyncClient):
    user = await create_test_user(client)

    assert user["email"] == DEFAULT_USER.email
    assert "id" in user
    assert "password" not in user
    assert "password_hash" not in user


@pytest.mark.anyio
async def test_create_user_duplicate_email(client: AsyncClient):
    await create_test_user(client)

    response = await client.post(
        "/api/v1/users",
        json={
            "first_name": "first-name",
            "last_name": "last-name",
            "email": DEFAULT_USER.email,
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

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == DEFAULT_USER.email
    assert "id" in data
    assert "password" not in data
    assert "password_hash" not in data


@pytest.mark.anyio
async def test_update_me_success(client: AsyncClient):
    user = await create_test_user(client)
    token = await login_user(client, user["id"])
    header = auth_header(token)

    response = await client.patch(
        "/api/v1/users/me",
        json={"first_name": "first-name-edited", "last_name": "last-name-edited"},
        headers=header,
    )

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["email"] == DEFAULT_USER.email
    assert data["first_name"] == "first-name-edited"
    assert data["last_name"] == "last-name-edited"

    response = await client.patch(
        "/api/v1/users/me",
        json={"last_name": "last-name"},
        headers=header,
    )

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["email"] == DEFAULT_USER.email
    assert data["last_name"] == "last-name"


@pytest.mark.anyio
async def test_update_me_no_data(client: AsyncClient):
    user = await create_test_user(client)
    token = await login_user(client, user["id"])
    header = auth_header(token)

    response = await client.patch(
        "/api/v1/users/me",
        json={},
        headers=header,
    )

    assert response.status_code == 400
    assert response.json()["message"] == "No fields provided for update."


@pytest.mark.anyio
async def test_delete_me_success(client: AsyncClient):
    user = await create_test_user(client)
    token = await login_user(client, user["id"])
    header = auth_header(token)

    response = await client.delete(
        "/api/v1/users/me",
        headers=header,
    )

    assert response.status_code == 204


@pytest.mark.anyio
async def test_change_password_success(client: AsyncClient):
    user = await create_test_user(client)
    token = await login_user(client, user["id"])
    header = auth_header(token)

    new_password = "String1234"

    response = await client.post(
        "/api/v1/users/me/change-password",
        json={
            "current_password": DEFAULT_USER.password,
            "new_password": new_password,
        },
        headers=header,
    )

    assert response.status_code == 204

    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": user["id"],
            "password": new_password,
        },
        headers=header,
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert "token_type" in data


@pytest.mark.anyio
async def test_change_password_same_password(client: AsyncClient):
    user = await create_test_user(client)
    token = await login_user(client, user["id"])
    header = auth_header(token)

    response = await client.post(
        "/api/v1/users/me/change-password",
        json={
            "current_password": DEFAULT_USER.password,
            "new_password": DEFAULT_USER.password,
        },
        headers=header,
    )

    assert response.status_code == 422
    assert response.json()["message"] == "Validation failed"
