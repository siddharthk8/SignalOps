from unittest.mock import AsyncMock, patch

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


@pytest.mark.anyio
async def test_forgot_and_reset_password_success(client: AsyncClient):
    await create_test_user(client)

    with patch(
        "app.domains.auth.service.password.send_reset_password_email",
        new_callable=AsyncMock,
    ) as mock_send:
        response = await client.post(
            "/api/v1/auth/forgot-password",
            json={"email": DEFAULT_USER.email},
        )

        assert response.status_code == 202
        data = response.json()
        assert (
            data["message"]
            == "If an account exists with this email address, you will receive password reset instructions shortly."
        )

        mock_send.assert_awaited_once()
        call_kwargs = mock_send.call_args.kwargs
        assert call_kwargs["to_email"] == DEFAULT_USER.email
        assert call_kwargs["first_name"] == DEFAULT_USER.first_name
        assert "token" in call_kwargs

        token = call_kwargs["token"]
        new_password = "String1234"

        response = await client.post(
            "/api/v1/auth/reset-password",
            json={"token": token, "new_password": new_password},
        )

        assert response.status_code == 200
        data = response.json()
        assert (
            data["message"]
            == "Your password has been reset successfully. You can now log in using your new password."
        )


@pytest.mark.anyio
async def test_forgot_password_reach_threshold(client: AsyncClient):
    await create_test_user(client)

    with patch(
        "app.domains.auth.service.password.send_reset_password_email",
        new_callable=AsyncMock,
    ) as _:
        response = await client.post(
            "/api/v1/auth/forgot-password",
            json={"email": DEFAULT_USER.email},
        )

        assert response.status_code == 202
        data = response.json()
        assert (
            data["message"]
            == "If an account exists with this email address, you will receive password reset instructions shortly."
        )

        response = await client.post(
            "/api/v1/auth/forgot-password",
            json={"email": DEFAULT_USER.email},
        )

        assert response.status_code == 429
        data = response.json()
        assert data["message"] == "Too many password reset requests."
