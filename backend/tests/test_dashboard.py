import pytest
from httpx import AsyncClient

from tests.conftest import auth_header, create_test_user, login_user


@pytest.mark.anyio
async def test_dashboard_success(client: AsyncClient):
    user = await create_test_user(client)
    access_token, _ = await login_user(client, user["email"])
    header = auth_header(access_token)

    response = await client.get(
        "/api/v1/dashboard",
        headers=header,
    )

    assert response.status_code == 200
    data = response.json()
    assert "source_apps_count" in data
    assert "incidents_count" in data
    assert "unresolved_incidents_count" in data
    assert "last_5_incidents" in data
    assert "daily_incidents_over_last_30_days" in data
