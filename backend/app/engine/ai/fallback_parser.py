import asyncio
from ipaddress import ip_address

from botocore.exceptions import ClientError
from fastapi.concurrency import run_in_threadpool
from pydantic import validate_email

from app.core.config import AI_MODEL_ID, AWS_MODEL_RETRY_ATTEMPTS
from app.engine.parsing import utils
from app.enums.common import Severity, SourceAppType
from app.enums.event import GenericEventType
from app.schemas.entity import Entity
from app.schemas.event import SemanticEvent
from app.schemas.log import PersistedLog
from app.shared.utils import (
    get_all_event_values_by_source_app,
    get_event_by_source_app,
)


class AIFallbackParser:
    """
    AI-powered semantic normalization fallback parser.

    Pipeline:
        unresolved logs
            ↓
        Bedrock semantic normalization
            ↓
        validated AI output
            ↓
        normalized semantic events
    """

    def __init__(self, client):
        # boto3 client
        self.client = client

    async def parse(
        self,
        unresolved_logs: list[tuple[int, PersistedLog]],
        source_app: SourceAppType,
    ) -> list[SemanticEvent]:
        event_types = get_all_event_values_by_source_app(source_app)
        severity_types = [s.value for s in Severity]

        payload = []

        for idx, log in unresolved_logs:
            normalized_log = log.model_dump(mode="json")

            payload.append(
                {
                    "log_id": idx,
                    "content": normalized_log,
                }
            )

        prompt = f"""
You are a deterministic log normalization engine.

STRICT INSTRUCTIONS (must follow exactly):

TASK
Convert each input log into exactly ONE normalized semantic event.

OUTPUT METHOD
You MUST return output ONLY via the tool: normalize_logs
No extra text, no explanation, no markdown, no reasoning.

---

HARD CONSTRAINTS
- Exactly ONE event per log_id
- Never omit any log_id
- Never merge logs
- Never split logs
- Never modify log_id in any way
- Never infer missing values (user, email, ip, session_id, request_id, token_id)
- Use ONLY allowed enum values
- Output must be valid tool JSON only

---

CLASSIFICATION PRIORITY (apply in order)

1. AUTHENTICATION
   - "login failed", "invalid credentials", "authentication failed" → LOGIN_FAIL
   - "login success", "authenticated" → LOGIN_SUCCESS

2. AUTHORIZATION
   - "access denied", "permission denied", "not authorized" → AUTHORIZATION_FAILURE

3. PAYMENT
   - "payment failed", "transaction declined", "charge failed" → PAYMENT_FAILED

4. ORDER

4. RATE LIMITING
   - "rate limit", "too many requests", "throttled" → RATE_LIMIT_EXCEEDED

5. CRASH / SYSTEM FAILURE
   - "fatal", "exception", "crash", "service stopped" → SERVER_CRASH

6. OTHERWISE
   → UNKNOWN (only if no clear match)

---

SEVERITY RULES
- CRITICAL → SERVER_CRASH, PAYMENT_FAILED
- HIGH → LOGIN_FAIL, AUTHORIZATION_FAILURE
- MEDIUM → RATE_LIMIT_EXCEEDED
- LOW → LOGIN_SUCCESS
- Default → MEDIUM if unclear

---

CONFIDENCE RULES
- 0.90 – 1.00 → explicit match in log text
- 0.60 – 0.89 → partial/indirect match
- < 0.60 → use UNKNOWN event_type
- If event_type = OTHER → confidence must be ≤ 0.70

---

ENTITY EXTRACTION RULES
Only extract if explicitly present in log text:
- user
- email
- ip
- session_id
- request_id
- token_id

DO NOT INFER ANY OF THESE.

---

CONSISTENCY RULE
Same log input must always produce identical output.

---

ALLOWED ENUMS

Event types:
{event_types}

Severity types:
{severity_types}

---

INPUT LOGS
{payload}
"""

        for attempt in range(AWS_MODEL_RETRY_ATTEMPTS):
            try:
                response = await run_in_threadpool(
                    self.client.converse,
                    modelId=AI_MODEL_ID,
                    # system=[]
                    messages=[
                        {
                            "role": "user",
                            "content": [{"text": prompt}],
                        }
                    ],
                    inferenceConfig={
                        "temperature": 0,
                        "topP": 0.1,
                        "maxTokens": 4000,
                    },
                    toolConfig={
                        "tools": [
                            {
                                "toolSpec": {
                                    "name": "normalize_logs",
                                    "description": (
                                        "Normalize application logs "
                                        "into semantic events."
                                    ),
                                    "inputSchema": {
                                        "json": {
                                            "type": "object",
                                            "properties": {
                                                "events": {
                                                    "type": "array",
                                                    "items": {
                                                        "type": "object",
                                                        "properties": {
                                                            "log_id": {
                                                                "type": "integer"
                                                            },
                                                            "event_type": {
                                                                "type": "string",
                                                                "enum": event_types,
                                                            },
                                                            "severity": {
                                                                "type": "string",
                                                                "enum": severity_types,
                                                            },
                                                            "confidence": {
                                                                "type": "number"
                                                            },
                                                            "user": {
                                                                "type": [
                                                                    "string",
                                                                    "null",
                                                                ]
                                                            },
                                                            "email": {
                                                                "type": [
                                                                    "string",
                                                                    "null",
                                                                ]
                                                            },
                                                            "ip": {
                                                                "type": [
                                                                    "string",
                                                                    "null",
                                                                ]
                                                            },
                                                            "session_id": {
                                                                "type": [
                                                                    "string",
                                                                    "null",
                                                                ]
                                                            },
                                                            "request_id": {
                                                                "type": [
                                                                    "string",
                                                                    "null",
                                                                ]
                                                            },
                                                            "token_id": {
                                                                "type": [
                                                                    "string",
                                                                    "null",
                                                                ]
                                                            },
                                                        },
                                                        "required": [
                                                            "log_id",
                                                            "event_type",
                                                            "severity",
                                                            "confidence",
                                                        ],
                                                        "additionalProperties": False,
                                                    },
                                                }
                                            },
                                            "required": ["events"],
                                            "additionalProperties": False,
                                        }
                                    },
                                }
                            }
                        ],
                        "toolChoice": {"any": {}},
                    },
                )

                content = response["output"]["message"]["content"]

                tool_blocks = [
                    block.get("toolUse") for block in content if "toolUse" in block
                ]
                if not tool_blocks:
                    raise ValueError("Model did not return tool output")

                raw_events = tool_blocks[0]["input"].get("events")

                # print("CINT: ", raw_events)
                if not isinstance(raw_events, list):
                    raise ValueError("Invalid tool output format")

                llm_map = {}

                for item in raw_events:
                    if not isinstance(item, dict):
                        continue

                    log_id = item.get("log_id")
                    try:
                        confidence = float(item.get("confidence", 0.0))
                    except Exception:
                        confidence = 0.0

                    confidence = max(
                        0.0,
                        min(confidence, 1.0),
                    )
                    item["confidence"] = confidence
                    llm_map[log_id] = item

                results = []

                for idx, log in unresolved_logs:
                    item = llm_map.get(idx, {})

                    try:
                        event_type = get_event_by_source_app(
                            source_app,
                            item.get("event_type"),
                        )
                    except Exception:
                        event_type = GenericEventType.UNKNOWN

                    if item.get("confidence", 0.0) < 0.35:
                        event_type = GenericEventType.UNKNOWN

                    try:
                        severity = Severity(item.get("severity", Severity.MEDIUM.value))
                    except Exception:
                        severity = Severity.MEDIUM

                    raw_ip = item.get("ip", None)

                    try:
                        parsed_ip = ip_address(raw_ip) if raw_ip else None
                    except Exception:
                        parsed_ip = None

                    if parsed_ip is None:
                        parsed_ip = utils.get_ip_address(log)

                    user = item.get("user", "null")
                    if user == "null":
                        user = utils.get_user(log)

                    email = item.get("email", "null")
                    if email == "null":
                        email = utils.get_email(log)
                    else:
                        try:
                            validate_email(email)
                        except Exception:
                            email = utils.get_email(log)

                    session_id = item.get("session_id", "null")
                    if session_id == "null":
                        session_id = utils.get_session_id(log)

                    request_id = item.get("request_id", "null")
                    if request_id == "null":
                        request_id = utils.get_request_id(log)

                    token_id = item.get("token_id", "null")
                    if token_id == "null":
                        token_id = utils.get_token_id(log)

                    results.append(
                        SemanticEvent(
                            sequence=idx,
                            source_app=source_app,
                            event_type=event_type,
                            severity=severity,
                            confidence=item.get(
                                "confidence",
                                0.0,
                            ),
                            timestamp=utils.get_timestamp(log),
                            persisted_log=log,
                            entity=Entity(
                                ip_address=parsed_ip,
                                user=user,
                                email=email,
                                session_id=session_id,
                                request_id=request_id,
                                token_id=token_id,
                            ),
                        )
                    )

                return results

            except ClientError:
                if attempt < AWS_MODEL_RETRY_ATTEMPTS - 1:
                    await asyncio.sleep(2**attempt)

            except Exception:
                raise

        raise RuntimeError("AI fallback parser unavailable.")
