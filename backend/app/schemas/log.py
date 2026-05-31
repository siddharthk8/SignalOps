from datetime import UTC, datetime
from typing import Annotated

from pydantic import (
    AliasChoices,
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    IPvAnyAddress,
    StringConstraints,
)

from app.enums.common import SourceAppType
from app.enums.logs import LogLevel
from app.shared.constants import (
    ENTITY_USER_ALIASES,
    INCOMING_LOG_IP_ALIASES,
    INCOMING_LOG_MESSAGE_ALIASES,
    INCOMING_LOG_SESSION_ALIASES,
    INCOMING_LOG_TIMESTAMP_ALIASES,
    INCOMING_LOG_TOKEN_ALIASES,
)

LOG_CONSTRAINT = StringConstraints(
    strict=True,
    min_length=5,
    max_length=500,
)


TextLogField = Annotated[str, LOG_CONSTRAINT]
MessageField = Annotated[
    TextLogField,
    Field(validation_alias=AliasChoices(*INCOMING_LOG_MESSAGE_ALIASES)),
]
UserField = Annotated[
    str | None,
    StringConstraints(min_length=1, max_length=100),
    Field(validation_alias=AliasChoices(*ENTITY_USER_ALIASES)),
]
RequestIdField = Annotated[
    str,
    StringConstraints(min_length=5, max_length=100),
]
IPField = Annotated[
    IPvAnyAddress | None,
    Field(
        validation_alias=AliasChoices(*INCOMING_LOG_IP_ALIASES),
    ),
]
SessionIDField = Annotated[
    str | None,
    StringConstraints(min_length=5, max_length=100),
    Field(default=None, validation_alias=AliasChoices(*INCOMING_LOG_SESSION_ALIASES)),
]
TokenIDField = Annotated[
    str | None,
    StringConstraints(min_length=5, max_length=100),
    Field(validation_alias=AliasChoices(*INCOMING_LOG_TOKEN_ALIASES)),
]
TimestampField = Annotated[
    datetime | None,
    Field(validation_alias=AliasChoices(*INCOMING_LOG_TIMESTAMP_ALIASES)),
]
EmailField = EmailStr


class LogBase(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        use_enum_values=True,
        extra="ignore",
        frozen=True,
    )


class JSONIncomingLog(LogBase):
    message: MessageField
    level: LogLevel | None = None
    timestamp: TimestampField = None
    user: UserField = None
    email: EmailStr | None = None
    ip_address: IPField = None
    session_id: SessionIDField = None
    token_id: TokenIDField = None
    request_id: RequestIdField | None = None

    model_config = ConfigDict(
        # Just a sample request body for the docs UI; it doesn't affect validation.
        json_schema_extra={
            "example": {
                "message": "Testing Log",
                "level": LogLevel.INFO,
                "timestamp": datetime.now(UTC).isoformat(),
                "user": None,
                "email": None,
                "ip_address": None,
                "session_id": None,
                "token_id": None,
                "request_id": None,
            }
        }
    )


type LogField = TextLogField | JSONIncomingLog
LogsField = Annotated[
    list[LogField],
    Field(
        min_length=1,
        max_length=100,
        description="Batch of logs",
    ),
]


class LogBatchRequest(LogBase):
    source_app: SourceAppType
    logs: LogsField
