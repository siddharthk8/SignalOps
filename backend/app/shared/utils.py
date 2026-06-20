from app.enums.common import SourceAppType
from app.enums.event import (
    AuthEventType,
    GenericEventType,
    OrderEventType,
    PaymentEventType,
)
from app.enums.incident import IncidentType

EVENT_DOMAIN_MAP = {
    "auth-app": AuthEventType,
    "payment-app": PaymentEventType,
    "order-app": OrderEventType,
}


def get_all_event_values_by_source_app(source_app: SourceAppType) -> list[str]:
    if source_app.value == SourceAppType.AUTH_APP:
        events = [e.value for e in AuthEventType]

    if source_app.value == SourceAppType.ORDER_APP:
        events = [e.value for e in OrderEventType]

    if source_app.value == SourceAppType.PAYMENT_APP:
        events = [e.value for e in PaymentEventType]

    generic_events = [e.value for e in GenericEventType]
    return [*events, *generic_events]


def get_all_event_values() -> list[str]:
    events = (
        [e.value for e in AuthEventType]
        + [e.value for e in OrderEventType]
        + [e.value for e in PaymentEventType]
        + [e.value for e in GenericEventType]
    )

    return events


def get_events_by_source_app(source_app: SourceAppType):
    return [e.value for e in EVENT_DOMAIN_MAP[source_app]]


def get_event_by_source_app(source_app: SourceAppType, event_value: str):
    enum_cls = EVENT_DOMAIN_MAP[source_app]

    try:
        return enum_cls(event_value)
    except ValueError:
        try:
            return GenericEventType(event_value)
        except ValueError:
            return GenericEventType.UNKNOWN


def get_all_incident_type_values() -> list[str]:
    """
    Returns all incident types for AI prompting + validation.
    """

    return [i.value for i in IncidentType]
