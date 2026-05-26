from datetime import datetime
from typing import Annotated, Any

from pydantic import BaseModel, Field, StringConstraints

from app.enums.common import Severity, SourceAppType
from app.enums.rule import SignalStatus
from app.schemas.entity import Entity
from app.schemas.event import SequenceField
from app.shared.constants import ALL_SIGNAL_TYPES

ConfidenceField = Annotated[
    float,
    Field(ge=0.0, le=1.0),
]
SignalDescriptionField = Annotated[
    str,
    StringConstraints(min_length=3, strip_whitespace=True),
]


class Signal(BaseModel):
    signal_type: ALL_SIGNAL_TYPES
    severity: Severity
    status: SignalStatus = SignalStatus.ACTIVE
    confidence: ConfidenceField
    supporting_events: list[SequenceField]
    source_app: SourceAppType
    entity: Entity
    metadata: dict[str, Any] = {}
    triggered_at: datetime
    resolved_at: datetime | None = None
