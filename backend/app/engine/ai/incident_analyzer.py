import asyncio

from botocore.exceptions import ClientError
from fastapi.concurrency import run_in_threadpool

from app.core.config import settings
from app.enums.common import Severity, SourceAppType
from app.schemas.analysis import IncidentAnalysis
from app.schemas.incident import Incident
from app.shared.utils import get_all_incident_type_values


class AIIncidentAnalyzer:
    """
    AI-powered incident analysis engine.

    INPUT:
        list[Incident]

    OUTPUT:
        list[IncidentAnalysis]
    """

    def __init__(self, client):
        # boto3 client
        self.client = client

    async def analyze(
        self,
        *,
        incidents: list[Incident],
        source_app: SourceAppType,
        ai_analyses: list[IncidentAnalysis],
    ) -> None:
        if len(incidents) == 0:
            return

        allowed_incident_types = get_all_incident_type_values()

        payload = [
            {
                "incident_index": idx,
                "incident_type": incident.incident_type,
                "severity": incident.severity,
                "confidence": incident.confidence,
                "source_app": source_app,
                "entities": [e.model_dump() for e in incident.entities],
                "signals": [
                    {
                        "signal_type": s.signal_type,
                        "confidence": s.confidence,
                        "triggered_at": str(s.triggered_at),
                        "metadata": s.metadata,
                    }
                    for s in incident.related_signals
                ],
                "summary": incident.summary,
            }
            for idx, incident in enumerate(incidents)
        ]

        prompt = f"""You are an expert Site Reliability Engineer (SRE) and incident analyst.

You will analyze MULTIPLE fully correlated incidents from an observability system.

STRICT RULES:

* Do NOT hallucinate new data.
* Do NOT assume missing fields.
* Use ONLY information contained within the specific incident being analyzed.
* Analyze EACH incident completely independently.
* Treat every incident as an isolated case.
* NEVER use entities, signals, metadata, summaries, root causes, impacts, recommendations, or classifications from one incident when analyzing another incident.
* NEVER compare incidents to each other.
* NEVER merge incidents together.
* NEVER infer relationships between incidents unless those relationships are explicitly present in that incident's data.
* If information required for analysis is not present in a specific incident, state that it cannot be determined from the available data.
* Preserve incident ordering.
* Return EXACTLY one analysis result per incident.
* The output for incident N must be derived only from the data provided for incident N.
* Be deterministic and structured.
* Output ONLY via tool call: analyze_incidents.

---

TASK:

For EACH incident independently:

1. Generate a human-readable summary.
2. Determine the most probable root cause using only that incident's data.
3. Assess business impact using only that incident's data.
4. Validate severity (may upgrade or downgrade if justified by that incident's data).
5. Recommend remediation and investigation actions specific to that incident.
6. Validate or correct the incident classification.

---

ANALYSIS ISOLATION REQUIREMENT:

Assume every incident was collected from a completely different system.

Before generating an analysis for an incident:

* Ignore all previous incidents.
* Ignore all subsequent incidents.
* Use only the fields contained in the current incident.
* Do not reuse conclusions from another incident.
* Do not generalize findings across incidents.

If two incidents appear similar, analyze them separately and independently.

---

ALLOWED INCIDENT TYPES:
{allowed_incident_types}

---

INPUT INCIDENTS:
{payload}
"""

        for attempt in range(settings.bedrock_model_retry_attempts):
            try:
                response = await run_in_threadpool(
                    self.client.converse,
                    modelId=settings.bedrock_model_id,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "text": prompt,
                                }
                            ],
                        }
                    ],
                    inferenceConfig={
                        "temperature": 0,
                        "topP": 0.1,
                        "maxTokens": 5000,
                    },
                    toolConfig={
                        "tools": [
                            {
                                "toolSpec": {
                                    "name": "analyze_incidents",
                                    "description": (
                                        "Generate structured incident analyses for multiple observability incidents."
                                    ),
                                    "inputSchema": {
                                        "json": {
                                            "type": "object",
                                            "properties": {
                                                "analyses": {
                                                    "type": "array",
                                                    "minItems": len(incidents),
                                                    "maxItems": len(incidents),
                                                    "items": {
                                                        "type": "object",
                                                        "properties": {
                                                            "incident_index": {
                                                                "type": "integer"
                                                            },
                                                            "summary": {
                                                                "type": "string"
                                                            },
                                                            "root_cause": {
                                                                "type": "string"
                                                            },
                                                            "business_impact": {
                                                                "type": "array",
                                                                "items": {
                                                                    "type": "string"
                                                                },
                                                            },
                                                            "severity": {
                                                                "type": "string",
                                                                "enum": [
                                                                    s.value
                                                                    for s in Severity
                                                                ],
                                                            },
                                                            "confidence": {
                                                                "type": "number"
                                                            },
                                                            "recommendations": {
                                                                "type": "array",
                                                                "items": {
                                                                    "type": "string"
                                                                },
                                                            },
                                                            "incident_type": {
                                                                "type": "string",
                                                                "enum": allowed_incident_types,
                                                            },
                                                        },
                                                        "required": [
                                                            "incident_index",
                                                            "summary",
                                                            "root_cause",
                                                            "business_impact",
                                                            "severity",
                                                            "confidence",
                                                            "recommendations",
                                                            "incident_type",
                                                        ],
                                                        "additionalProperties": False,
                                                    },
                                                }
                                            },
                                            "required": [
                                                "analyses",
                                            ],
                                            "additionalProperties": False,
                                        }
                                    },
                                }
                            }
                        ],
                        "toolChoice": {
                            "any": {},
                        },
                    },
                )

                content = response["output"]["message"]["content"]

                tool_blocks = [
                    block.get("toolUse") for block in content if "toolUse" in block
                ]

                if not tool_blocks:
                    raise ValueError("No tool output returned from AI")

                data = tool_blocks[0]["input"]

                analyses_data = data.get(
                    "analyses",
                    [],
                )

                if len(analyses_data) != len(incidents):
                    # print("analyses_data len:", len(analyses_data))
                    # print("incidents len:", len(incidents))
                    # print("analyses_data:\n", (analyses_data), "\n")
                    # print("incidents:\n", (incidents), "\n")

                    raise ValueError(
                        f"Expected {len(incidents)} analyses, got {len(analyses_data)}"
                    )

                analyses_data = sorted(
                    analyses_data,
                    key=lambda x: x["incident_index"],
                )

                for item in analyses_data:
                    idx = item["incident_index"]

                    if idx >= len(incidents):
                        raise ValueError(f"Invalid incident_index returned: {idx}")

                    original_incident = incidents[idx]

                    ai_analyses.append(
                        IncidentAnalysis(
                            summary=item.get(
                                "summary",
                                original_incident.summary,
                            ),
                            root_cause=item.get(
                                "root_cause",
                                "Unknown",
                            ),
                            business_impact=item.get(
                                "business_impact",
                                [],
                            ),
                            severity=Severity(
                                item.get(
                                    "severity",
                                    original_incident.severity,
                                )
                            ),
                            confidence=float(
                                item.get(
                                    "confidence",
                                    0.0,
                                )
                            ),
                            recommendations=item.get(
                                "recommendations",
                                [],
                            ),
                            incident_type=item.get(
                                "incident_type",
                                original_incident.incident_type,
                            ),
                        )
                    )

                return

            except ClientError:
                if attempt < settings.bedrock_model_retry_attempts - 1:
                    await asyncio.sleep(2**attempt)
                else:
                    raise

            except Exception:
                raise
