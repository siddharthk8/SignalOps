from datetime import datetime
from typing import Annotated, Any

from pydantic import BaseModel, Field

from app.enums.common import Severity, SourceAppType
from app.schemas.entity import Entity
from app.schemas.log import LogField
from app.shared.constants import ALL_EVENT_TYPES

SequenceField = Annotated[int, Field(ge=0)]
ConfidenceField = Annotated[float, Field(ge=0.0, le=1.0)]


class SemanticEvent(BaseModel):
    sequence: SequenceField
    source_app: SourceAppType
    event_type: ALL_EVENT_TYPES
    confidence: ConfidenceField
    severity: Severity
    timestamp: datetime | None = None
    raw_log: LogField
    entity: Entity
    metadata: dict[str, Any] | None = None
