from enum import StrEnum


class SourceAppType(StrEnum):
    AUTH_APP = "auth-app"
    PAYMENT_APP = "payment-app"
    ORDER_APP = "order-app"


class Severity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
