from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from .common import LogStatus, SourceAppType

LOG_STRING = StringConstraints(
    strip_whitespace=True,
    strict=True,
    min_length=5,
    max_length=500,
)
LogField = Annotated[str, LOG_STRING]
LogsField = Annotated[
    list[LogField],
    Field(
        min_length=1,
        max_length=100,
        description="Batch of logs",
    ),
]


class LogBase(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        use_enum_values=True,
        validate_assignment=True,
        extra="forbid",
    )


class LogBatchRequest(LogBase):
    source_app: SourceAppType
    logs: LogsField


class LogBatchResponse(LogBase):
    status: LogStatus
    timestamp: datetime
