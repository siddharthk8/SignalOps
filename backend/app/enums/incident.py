from enum import StrEnum


class IncidentType(StrEnum):
    ACCOUNT_SECURITY = "account_security"
    PAYMENT_OUTAGE = "payment_outage"
    SERVICE_DEGRADATION = "service_degradation"
    POTENTIAL_FRAUD = "potential_fraud"
    PLATFORM_INSTABILITY = "platform_instability"
    INFORMATIONAL = "informational"


class IncidentStatus(StrEnum):
    OPEN = "open"
    ACKNOWLEDGED = "acknowledged"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    FALSE_POSITIVE = "false_positive"
