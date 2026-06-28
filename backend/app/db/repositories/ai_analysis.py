import json

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.ai_analysis import AIAnalysis
from app.schemas.analysis import IncidentAnalysis
from app.schemas.incident import Incident


class AIAnalysisRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(
        self,
        *,
        batch_id: int,
        incidents: list[Incident],
        ai_analyses: list[IncidentAnalysis],
    ) -> None:
        ai_analysis_models: list[AIAnalysis] = []

        for i, a in enumerate(ai_analyses):
            analyzed_payload = a.model_dump(exclude={"id"})
            analyzed_payload["batch_id"] = batch_id
            analyzed_payload["severity"] = a.severity.value
            analyzed_payload["incident_type"] = a.incident_type.value
            analyzed_payload["business_impact"] = json.dumps(a.business_impact)
            analyzed_payload["recommendations"] = json.dumps(a.recommendations)

            ai_analysis_model = AIAnalysis(
                **analyzed_payload, incident_id=incidents[i].id
            )
            ai_analysis_models.append(ai_analysis_model)
            self.db.add(ai_analysis_model)

        await self.db.flush()
        for i, a_model in enumerate(ai_analysis_models):
            ai_analyses[i].id = a_model.id
