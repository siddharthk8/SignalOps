import asyncio
from ipaddress import ip_address

from botocore.exceptions import ClientError
from fastapi.concurrency import run_in_threadpool
from pydantic import validate_email

from app.core.config import settings
from app.engine.parsing import utils
from app.engine.parsing.base import BaseParser
from app.enums.common import Severity, SourceAppType
from app.enums.event import GenericEventType, ParsingMethodType
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
            if log.log_format == "string":
                normalized_log = log.message
            else:
                normalized_log = log.model_dump(mode="json")

            payload.append(
                {
                    "id": idx,
                    "log": normalized_log,
                }
            )

        prompt = f"""
You are a deterministic log normalization engine.

TASK

Convert each input log into exactly ONE normalized event.

OUTPUT

Respond ONLY using the normalize_logs tool.

RULES

* Exactly one event per input id
* Never omit, modify, merge, or split ids
* Use only allowed event types and severity values
* Never invent event types
* Never infer missing entity values

CLASSIFICATION

Select the most semantically accurate event_type from the allowed taxonomy.

* Match based on meaning, not exact wording
* Synonyms and equivalent phrasing are valid matches
* Prefer specific events over generic events
* Use "unknown" only when no reasonable taxonomy match exists

SEVERITY

Assign the most appropriate severity based on the event meaning.

CONFIDENCE

Confidence reflects confidence in the selected classification.

* High confidence for clear semantic matches
* Low confidence only when classification is genuinely uncertain
* If confidence < 0.60, event_type must be "unknown"

ENTITY EXTRACTION

Extract only if explicitly present:

* user
* email
* ip
* session_id
* request_id
* token_id

Do not infer or guess missing values.

ALLOWED EVENT TYPES

{event_types}

ALLOWED SEVERITIES

{severity_types}

INPUT LOGS

{payload}
"""

        for attempt in range(settings.aws_ai_model_retry_attempts):
            try:
                response = await run_in_threadpool(
                    self.client.converse,
                    modelId=settings.aws_ai_model_id,
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
                                        "Normalize application logs into semantic events."
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
                                                            "id": {"type": "integer"},
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
                                                            "id",
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

                # print("raw_events: ", raw_events)
                if not isinstance(raw_events, list):
                    raise ValueError("Invalid tool output format")

                llm_map = {}

                for item in raw_events:
                    if not isinstance(item, dict):
                        continue

                    id = item.get("id")
                    try:
                        confidence = float(item.get("confidence", 0.0))
                    except Exception:
                        confidence = 0.0

                    confidence = max(
                        0.0,
                        min(confidence, 1.0),
                    )
                    item["confidence"] = confidence
                    llm_map[id] = item

                results = []

                for idx, log in unresolved_logs:
                    item = llm_map.get(idx, {})

                    event_type = get_event_by_source_app(
                        source_app,
                        item.get("event_type"),
                    )

                    if item.get("confidence", 0.0) < BaseParser.MIN_CONFIDENCE:
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
                            event_type=event_type,
                            severity=severity,
                            parsing_method=ParsingMethodType.AI,
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
                if attempt < settings.aws_ai_model_retry_attempts - 1:
                    await asyncio.sleep(2**attempt)

            except Exception:
                raise

        raise RuntimeError("AI fallback parser unavailable.")
