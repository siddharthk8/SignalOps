import pytest
from httpx import AsyncClient

from tests.conftest import (
    DEFAULT_SOURCE_APP,
    auth_header,
    create_test_user,
    login_user,
)

NORMALIZE_LOGS_RESPONSE = {
    "output": {
        "message": {
            "content": [
                {
                    "toolUse": {
                        "input": {
                            "events": [
                                {
                                    "severity": "low",
                                    "event_type": "other",
                                    "confidence": 0.8,
                                    "id": 4,
                                }
                            ]
                        },
                    }
                }
            ],
        }
    }
}

ANALYZE_INCIDENTS_RESPONSE = {
    "output": {
        "message": {
            "content": [
                {
                    "toolUse": {
                        "input": {
                            "analyses": [
                                {
                                    "summary": "An excessive number of authentication failures originating from IP address 192.168.1.10 within a 5-minute window between 09:00 UTC and 09:01 UTC on June 28, 2026, triggered a high-severity security alert.",
                                    "severity": "high",
                                    "incident_type": "account_security",
                                    "incident_index": 0,
                                    "confidence": 0.9,
                                    "business_impact": [
                                        "Potential account compromise if the failed attempts were malicious.",
                                        "Possible unauthorized access attempts.",
                                    ],
                                    "recommendations": [
                                        "Investigate the source IP address 192.168.1.10 to determine the nature of the failed login attempts.",
                                        "Review authentication logs for further details on the failed attempts (e.g., attempted passwords).",
                                        "Consider implementing rate limiting or account lockout policies for suspicious IP addresses.",
                                    ],
                                    "root_cause": "Excessive authentication failures from a single IP address likely indicate a brute-force attack or other malicious activity attempting to gain unauthorized access to user accounts.",
                                }
                            ]
                        },
                    }
                }
            ],
        }
    }
}


@pytest.mark.anyio
async def test_ingest_logs_text_success(client: AsyncClient, mocked_bedrock_client):
    user = await create_test_user(client)
    access_token, _ = await login_user(client, user["id"])
    header = auth_header(access_token)

    response = await client.post(
        "/api/v1/source-apps",
        json={
            "name": DEFAULT_SOURCE_APP.name,
            "app_type": DEFAULT_SOURCE_APP.app_type,
        },
        headers=header,
    )
    source_app_id = response.json()["id"]

    mocked_bedrock_client.converse.side_effect = [
        NORMALIZE_LOGS_RESPONSE,
        ANALYZE_INCIDENTS_RESPONSE,
    ]

    response = await client.post(
        "/api/v1/logs",
        json={
            "source_app_id": source_app_id,
            "logs": [
                "2026-06-28T09:00:00Z WARN Login failed for username='alice' from IP 192.168.1.10",
                "2026-06-28T09:00:12Z WARN Login failed for username='alice' from IP 192.168.1.10",
                "2026-06-28T09:00:24Z WARN Login failed for username='alice' from IP 192.168.1.10",
                "2026-06-28T09:00:36Z WARN Login failed for username='alice' from IP 192.168.1.10",
                "Testing with random log",
                "2026-06-28T09:01:48Z WARN Login failed for username='alice' from IP 192.168.1.10",
            ],
        },
        headers=header,
    )

    assert response.status_code == 200
    data = response.json()[0]
    assert "id" in data
    assert "summary" in data
    assert "severity" in data
    assert "confidence" in data
    assert "business_impact" in data
    assert "recommendations" in data
    assert "root_cause" in data


@pytest.mark.anyio
async def test_ingest_logs_json_success(client: AsyncClient, mocked_bedrock_client):
    user = await create_test_user(client)
    access_token, _ = await login_user(client, user["id"])
    header = auth_header(access_token)

    response = await client.post(
        "/api/v1/source-apps",
        json={
            "name": DEFAULT_SOURCE_APP.name,
            "app_type": DEFAULT_SOURCE_APP.app_type,
        },
        headers=header,
    )
    source_app_id = response.json()["id"]

    mocked_bedrock_client.converse.side_effect = [
        NORMALIZE_LOGS_RESPONSE,
        ANALYZE_INCIDENTS_RESPONSE,
    ]

    response = await client.post(
        "/api/v1/logs",
        json={
            "source_app_id": source_app_id,
            "logs": [
                {
                    "message": "Login failed for username='alice' from IP 192.168.1.10",
                    "level": "warn",
                    "timestamp": "2026-06-28T09:00:00Z",
                    "user": "alice",
                    "email": None,
                    "ip_address": "192.168.1.10",
                    "session_id": None,
                    "token_id": None,
                    "request_id": None,
                },
                {
                    "message": "Login failed for username='alice' from IP 192.168.1.10",
                    "level": "warn",
                    "timestamp": "2026-06-28T09:00:12Z",
                    "user": "alice",
                    "email": None,
                    "ip_address": "192.168.1.10",
                    "session_id": None,
                    "token_id": None,
                    "request_id": None,
                },
                {
                    "message": "Login failed for username='alice' from IP 192.168.1.10",
                    "level": "warn",
                    "timestamp": "2026-06-28T09:00:24Z",
                    "user": "alice",
                    "email": None,
                    "ip_address": "192.168.1.10",
                    "session_id": None,
                    "token_id": None,
                    "request_id": None,
                },
                {
                    "message": "Login failed for username='alice' from IP 192.168.1.10",
                    "level": "warn",
                    "timestamp": "2026-06-28T09:00:36Z",
                    "user": "alice",
                    "email": None,
                    "ip_address": "192.168.1.10",
                    "session_id": None,
                    "token_id": None,
                    "request_id": None,
                },
                {
                    "message": "Testing with random log",
                    "level": None,
                    "timestamp": None,
                    "user": None,
                    "email": None,
                    "ip_address": None,
                    "session_id": None,
                    "token_id": None,
                    "request_id": None,
                },
                {
                    "message": "Login failed for username='alice' from IP 192.168.1.10",
                    "level": "warn",
                    "timestamp": "2026-06-28T09:01:48Z",
                    "user": "alice",
                    "email": None,
                    "ip_address": "192.168.1.10",
                    "session_id": None,
                    "token_id": None,
                    "request_id": None,
                },
            ],
        },
        headers=header,
    )

    assert response.status_code == 200
    data = response.json()[0]
    assert "id" in data
    assert "summary" in data
    assert "severity" in data
    assert "confidence" in data
    assert "business_impact" in data
    assert "recommendations" in data
    assert "root_cause" in data
