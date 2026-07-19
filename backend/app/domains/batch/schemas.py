from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, IPvAnyAddress

from app.enums.common import Severity
from app.enums.event import ParsingMethodType
from app.enums.incident import IncidentStatus, IncidentType
from app.enums.logs import LogLevel


class _BaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, frozen=True)


class LogResponse(_BaseModel):
    id: int
    message: str
    level: LogLevel | None
    timestamp: datetime | None
    user: str | None
    email: str | None
    ip_address: IPvAnyAddress | None
    session_id: str | None
    token_id: str | None
    request_id: str | None


class EntityResponse(_BaseModel):
    id: int
    user: str | None
    email: str | None
    ip_address: str | None
    session_id: str | None
    token_id: str | None
    request_id: str | None


class EventResponse(_BaseModel):
    id: int
    event_type: StrEnum
    confidence: float
    severity: Severity
    timestamp: datetime | None
    parsing_method: ParsingMethodType
    log_id: int
    entity_id: int | None


class SignalResponse(_BaseModel):
    id: int
    signal_type: StrEnum
    confidence: float
    triggered_at: datetime
    entity_id: int | None


class IncidentResponse(_BaseModel):
    id: int
    incident_type: IncidentType
    severity: Severity
    status: IncidentStatus
    confidence: float
    title: str
    summary: str
    detected_at: datetime
    updated_at: datetime
    resolved_at: datetime | None = None


class AIAnalysisResponse(_BaseModel):
    id: int
    incident_id: int | None
    summary: str
    root_cause: str
    business_impact: str
    recommendations: str
    severity: Severity
    confidence: float
    incident_type: IncidentType


class GetBatch(_BaseModel):
    id: int
    logs: list[LogResponse]
    entities: list[EntityResponse]
    events: list[EventResponse]
    signals: list[SignalResponse]
    incidents: list[IncidentResponse]
    ai_analyses: list[AIAnalysisResponse]
    created_at: datetime


class BatchesAIAnalysisResponse(_BaseModel):
    id: int
    severity: Severity
    confidence: float


class Batch(_BaseModel):
    id: int
    log_count: int
    ai_analyses: list[BatchesAIAnalysisResponse]
    created_at: datetime
