import asyncio

from botocore.exceptions import ClientError
from fastapi.concurrency import run_in_threadpool

from app.core.config import AI_MODEL_ID, AWS_MODEL_RETRY_ATTEMPTS
from app.enums.common import Severity, SourceAppType
from app.schemas.analysis import IncidentAnalysis
from app.schemas.incident import Incident
from app.shared.utils import get_all_incident_type_values


class AIIncidentAnalyzer:
    """
    AI-powered incident analysis engine.

    INPUT:
        Incident (already correlated + structured)

    OUTPUT:
        IncidentAnalysis (structured reasoning)
    """

    def __init__(self, client):
        # boto3 client
        self.client = client

    async def analyze(
        self, incident: Incident, source_app: SourceAppType
    ) -> IncidentAnalysis:

        allowed_incident_types = get_all_incident_type_values()

        payload = {
            # "incident_id": str(incident.incident_id),
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
                }
                for s in incident.related_signals
            ],
            "summary": incident.summary,
            "metadata_for_each_signal": [s.metadata for s in incident.related_signals],
        }

        prompt = f"""
You are an expert Site Reliability Engineer (SRE) and incident analyst.

You will analyze a fully correlated incident from an observability system.

STRICT RULES:
- Do NOT hallucinate new data
- Do NOT assume missing fields
- Use ONLY provided incident information
- Be deterministic and structured
- Output ONLY via tool call: analyze_incident

---

TASK:
Analyze the incident and produce operational intelligence:

1. Human-readable summary (improved if needed)
2. Probable root cause
3. Business impact
4. Severity validation (can upgrade/downgrade but must justify)
5. Recommended actions (step-by-step)
6. Incident classification check

---

ALLOWED INCIDENT TYPES:
{allowed_incident_types}

---

INPUT INCIDENT:
{payload}
"""

        for attempt in range(AWS_MODEL_RETRY_ATTEMPTS):
            try:
                response = await run_in_threadpool(
                    self.client.converse,
                    modelId=AI_MODEL_ID,
                    messages=[
                        {
                            "role": "user",
                            "content": [{"text": prompt}],
                        }
                    ],
                    inferenceConfig={
                        "temperature": 0,
                        "topP": 0.1,
                        "maxTokens": 3000,
                    },
                    toolConfig={
                        "tools": [
                            {
                                "toolSpec": {
                                    "name": "analyze_incident",
                                    "description": (
                                        "Generate structured incident analysis "
                                        "for observability platform."
                                    ),
                                    "inputSchema": {
                                        "json": {
                                            "type": "object",
                                            "properties": {
                                                "summary": {"type": "string"},
                                                "root_cause": {"type": "string"},
                                                "business_impact": {
                                                    "type": "array",
                                                    "items": {"type": "string"},
                                                },
                                                "severity": {
                                                    "type": "string",
                                                    "enum": [s.value for s in Severity],
                                                },
                                                "confidence": {"type": "number"},
                                                "recommendations": {
                                                    "type": "array",
                                                    "items": {"type": "string"},
                                                },
                                                "incident_type": {
                                                    "type": "string",
                                                    "enum": allowed_incident_types,
                                                },
                                            },
                                            "required": [
                                                "summary",
                                                "root_cause",
                                                "business_impact",
                                                "severity",
                                                "confidence",
                                                "recommendations",
                                                "incident_type",
                                            ],
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
                    raise ValueError("No tool output returned from AI")

                data = tool_blocks[0]["input"]

                # SAFE PARSING
                analysis = IncidentAnalysis(
                    # incident_id=incident.incident_id,
                    summary=data.get("summary", incident.summary),
                    root_cause=data.get("root_cause", "Unknown"),
                    business_impact=data.get("business_impact", "Unknown"),
                    severity=Severity(data.get("severity", incident.severity)),
                    confidence=float(data.get("confidence", 0.0)),
                    recommendations=data.get("recommendations", []),
                    incident_type=data.get(
                        "incident_type",
                        incident.incident_type,
                    ),
                )

                return analysis

            except ClientError:
                if attempt < AWS_MODEL_RETRY_ATTEMPTS - 1:
                    await asyncio.sleep(2**attempt)

            except Exception:
                raise

        raise RuntimeError("AI incident analysis failed.")
