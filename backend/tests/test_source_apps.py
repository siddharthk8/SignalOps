import pytest
from httpx import AsyncClient

from tests.conftest import DEFAULT_SOURCE_APP, auth_header, create_test_user, login_user


@pytest.mark.anyio
async def test_create_source_app_success(client: AsyncClient):
    user = await create_test_user(client)
    access_token, _ = await login_user(client, user["email"])
    header = auth_header(access_token)

    response = await client.post(
        "/api/v1/source-apps",
        json={
            "name": DEFAULT_SOURCE_APP.name,
            "app_type": DEFAULT_SOURCE_APP.app_type,
        },
        headers=header,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == DEFAULT_SOURCE_APP.name
    assert data["app_type"] == DEFAULT_SOURCE_APP.app_type
    assert "id" in data
    assert "created_at" in data


@pytest.mark.anyio
async def test_delete_source_app_success(client: AsyncClient):
    user = await create_test_user(client)
    access_token, _ = await login_user(client, user["email"])
    header = auth_header(access_token)

    response = await client.post(
        "/api/v1/source-apps",
        json={
            "name": DEFAULT_SOURCE_APP.name,
            "app_type": DEFAULT_SOURCE_APP.app_type,
        },
        headers=header,
    )

    assert response.status_code == 200

    response = await client.delete(
        f"/api/v1/source-apps/{response.json()['id']}",
        headers=header,
    )

    assert response.status_code == 204


@pytest.mark.anyio
async def test_delete_source_app_fail(client: AsyncClient):
    user = await create_test_user(client)
    access_token, _ = await login_user(client, user["email"])
    header = auth_header(access_token)

    response = await client.delete(
        "/api/v1/source-apps/545623",  # random id
        headers=header,
    )

    assert response.status_code == 404


@pytest.mark.anyio
async def test_get_source_apps_with_pagination(client: AsyncClient):
    user = await create_test_user(client)
    access_token, _ = await login_user(client, user["email"])
    header = auth_header(access_token)

    for i in range(10):
        response = await client.post(
            "/api/v1/source-apps",
            json={
                "name": f"{DEFAULT_SOURCE_APP.name} : {i}",
                "app_type": "auth-app"
                if i < 3
                else "order-app"
                if i < 7
                else "payment-app",
            },
            headers=header,
        )

        assert response.status_code == 200

    response = await client.get(
        "/api/v1/source-apps?skip=2&limit=2",
        headers=header,
    )

    assert response.status_code == 200
    data = response.json()
    assert "source_apps" in data
    assert data["total"] == 10
    assert data["skip"] == 2
    assert data["limit"] == 2
    assert data["has_more"] is True

    response = await client.get(
        "/api/v1/source-apps?skip=5&limit=3",
        headers=header,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 10
    assert data["has_more"] is True

    response = await client.get(
        "/api/v1/source-apps?skip=5&limit=5",
        headers=header,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 10
    assert data["has_more"] is False
