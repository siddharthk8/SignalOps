from datetime import datetime
from typing import Annotated, Any

from pydantic import BaseModel, Field

from app.enums.common import Severity, SourceAppType
from app.enums.incident import IncidentStatus, IncidentType
from app.schemas.entity import Entity
from app.schemas.signal import Signal

IncidentSummaryField = Annotated[str, Field(min_length=3)]
ConfidenceField = Annotated[
    float,
    Field(ge=0.0, le=1.0),
]


class Incident(BaseModel):
    incident_type: IncidentType
    severity: Severity
    status: IncidentStatus = IncidentStatus.OPEN
    confidence: ConfidenceField
    title: str
    summary: IncidentSummaryField
    source_apps: list[SourceAppType]
    entities: list[Entity]
    related_signals: list[Signal]  # modify this to store only signals ids when using DB
    metadata: dict[str, Any] = {}
    first_detected_at: datetime
    last_updated_at: datetime
    resolved_at: datetime | None = None
