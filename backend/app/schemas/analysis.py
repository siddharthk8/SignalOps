from pydantic import BaseModel, Field

from app.enums.common import Severity
from app.enums.incident import IncidentType


class IncidentAnalysis(BaseModel):
    """
    AI-generated structured analysis of a correlated incident.
    """

    id: int | None = None  # db
    summary: str
    root_cause: str
    business_impact: list[str]
    severity: Severity
    confidence: float = Field(ge=0.0, le=1.0)
    recommendations: list[str]
    incident_type: IncidentType
