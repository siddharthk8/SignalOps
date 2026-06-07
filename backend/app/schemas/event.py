from datetime import datetime
from typing import Annotated, Any

from pydantic import BaseModel, Field

from app.enums.common import Severity, SourceAppType
from app.enums.event import ParsingMethodType
from app.schemas.entity import Entity
from app.schemas.log import PersistedLog
from app.shared.constants import ALL_EVENT_TYPES

SequenceField = Annotated[int, Field(ge=0)]
ConfidenceField = Annotated[float, Field(ge=0.0, le=1.0)]


class SemanticEvent(BaseModel):
    id: int | None = None  # db id
    sequence: SequenceField
    source_app: SourceAppType
    event_type: ALL_EVENT_TYPES
    confidence: ConfidenceField
    severity: Severity
    timestamp: datetime | None = None
    persisted_log: PersistedLog
    parsing_method: ParsingMethodType
    entity: Entity
    metadata: dict[str, Any] | None = None
