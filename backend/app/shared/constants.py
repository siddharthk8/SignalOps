from app.enums.event import (
    AuthEventType,
    GenericEventType,
    OrderEventType,
    PaymentEventType,
)
from app.enums.rule import ApiAbuseSignalType, BruteForceSignalType

# common
ENTITY_USER_ALIASES = (
    "user",  # we also need to include the actual name of the field.
    "user_id",
    "username",
)

INCOMING_LOG_TIMESTAMP_ALIASES = ["ts", "timestamp"]
INCOMING_LOG_MESSAGE_ALIASES = ["message", "msg", "event"]
INCOMING_LOG_SESSION_ALIASES = ["session_id", "session", "sid"]
INCOMING_LOG_IP_ALIASES = ["ip", "ip_address", "internet_protocol"]


type ALL_EVENT_TYPES = (
    AuthEventType | OrderEventType | PaymentEventType | GenericEventType
)
type ALL_SIGNAL_TYPES = ApiAbuseSignalType | BruteForceSignalType
