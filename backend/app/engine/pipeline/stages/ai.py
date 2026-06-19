import boto3
from botocore.config import Config
from sqlalchemy.orm import Session

from app.db.repositories.ai_analysis import AIAnalysisRepository
from app.engine.ai.fallback_parser import AIFallbackParser
from app.engine.ai.incident_analyzer import AIIncidentAnalyzer
from app.enums.common import Severity, SourceAppType
from app.enums.incident import IncidentType
from app.schemas.analysis import IncidentAnalysis
from app.schemas.event import SemanticEvent
from app.schemas.incident import Incident
from app.schemas.log import PersistedLog


class AIStage:
    def __init__(self, db: Session):
        self.db = db

        self.client = boto3.client(
            "bedrock-runtime",
            region_name="ap-south-1",
            config=Config(
                retries={"max_attempts": 3},
                read_timeout=120,
                connect_timeout=20,
            ),
        )
        self.ai_fallback_parser = AIFallbackParser(self.client)
        self.ai_incident_analyzer = AIIncidentAnalyzer(self.client)
        self.ai_analysis_repo = AIAnalysisRepository(self.db)

    async def fallback_run(
        self, unresolved_logs: list[tuple[int, PersistedLog]], source_app: SourceAppType
    ) -> list[SemanticEvent]:
        ai_events = await self.ai_fallback_parser.parse(unresolved_logs, source_app)
        return ai_events

    async def run(
        self, incidents: list[Incident], source_app: SourceAppType
    ) -> list[IncidentAnalysis]:
        analyzed_incidents: list[IncidentAnalysis] = []

        for i in incidents:
            analyzed_incidents.append(
                await self.ai_incident_analyzer.analyze(i, source_app)
            )

        if len(analyzed_incidents) == 0:
            analyzed_incidents = [
                IncidentAnalysis(
                    summary=(
                        "No significant operational issues detected. "
                        "Observed signals appear consistent with expected application behavior."
                    ),
                    root_cause=(
                        "No root cause identified. Signal patterns do not indicate an active incident."
                    ),
                    business_impact=[
                        "No customer-facing impact detected.",
                        "Service availability and functionality appear normal.",
                    ],
                    severity=Severity.LOW,
                    confidence=0.9,
                    recommendations=[
                        "No immediate action required.",
                        "Continue routine monitoring.",
                        "Review trends periodically for emerging patterns.",
                    ],
                    incident_type=IncidentType.INFORMATIONAL,
                )
            ]

        # save ai_incidents in db
        self.ai_analysis_repo.save_ai_analysis(analyzed_incidents=analyzed_incidents)

        return analyzed_incidents
