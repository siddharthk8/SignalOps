import json

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.ai_analysis import AIAnalysis
from app.schemas.analysis import IncidentAnalysis


class AIAnalysisRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_ai_analysis(
        self, *, analyzed_incidents: list[IncidentAnalysis], batch_id: int
    ) -> None:

        for a in analyzed_incidents:
            analyzed_payload = a.model_dump()
            analyzed_payload["batch_id"] = batch_id
            analyzed_payload["severity"] = a.severity.value
            analyzed_payload["incident_type"] = a.incident_type.value
            analyzed_payload["business_impact"] = json.dumps(a.business_impact)
            analyzed_payload["recommendations"] = json.dumps(a.recommendations)

            ai_analysis_orm = AIAnalysis(**analyzed_payload)
            self.db.add(ai_analysis_orm)

        await self.db.flush()
