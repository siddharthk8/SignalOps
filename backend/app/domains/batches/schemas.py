from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.enums.common import Severity
from app.enums.incident import IncidentType


class _BaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, frozen=True)


class AIAnalysisResponse(_BaseModel):
    id: int
    summary: str
    root_cause: str
    business_impact: str
    severity: Severity
    confidence: float = Field(ge=0.0, le=1.0)
    recommendations: str
    incident_type: IncidentType


class Batch(_BaseModel):
    id: int
    ai_analysis: AIAnalysisResponse
    created_at: datetime
