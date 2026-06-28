import pytest
from httpx import AsyncClient

from tests.conftest import DEFAULT_USER, auth_header, create_test_user, login_user


@pytest.mark.anyio
async def test_login_success(client: AsyncClient):
    user = await create_test_user(client)

    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": user["id"],
            "password": DEFAULT_USER.password,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert "token_type" in data


@pytest.mark.anyio
async def test_login_missing_username(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/login",
        data={"password": DEFAULT_USER.password},
    )

    assert response.status_code == 422


@pytest.mark.anyio
async def test_login_missing_password(client: AsyncClient):
    user = await create_test_user(client)

    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": user["id"],
        },
    )

    assert response.status_code == 422


@pytest.mark.anyio
async def test_login_incorrect_password(client: AsyncClient):
    user = await create_test_user(client)

    response = await client.post(
        "/api/v1/auth/login",
        data={"username": user["id"], "password": "random_password"},
    )

    assert response.status_code == 401


@pytest.mark.anyio
async def test_login_nonexistent_user(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "a43b61cb-94e6-4b44-9f74-7d53f15d76cb",  # random uuid
            "password": "random_password",
        },
    )

    assert response.status_code == 401


@pytest.mark.anyio
async def test_refresh_access_token_success(client: AsyncClient):
    user = await create_test_user(client)
    _, refresh_token = await login_user(client, user["id"])

    response = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token},
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert "refresh_token" not in data


@pytest.mark.anyio
async def test_logout_success(client: AsyncClient):
    user = await create_test_user(client)
    access_token, refresh_token = await login_user(client, user["id"])
    header = auth_header(access_token)

    response = await client.post(
        "/api/v1/auth/logout", json={"refresh_token": refresh_token}, headers=header
    )

    assert response.status_code == 204


@pytest.mark.anyio
async def test_logout_all_success(client: AsyncClient):
    user = await create_test_user(client)
    access_token, _ = await login_user(client, user["id"])
    header = auth_header(access_token)

    response = await client.post(
        "/api/v1/auth/logout-all",
        headers=header,
    )

    assert response.status_code == 204
