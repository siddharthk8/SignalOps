from enum import StrEnum


class SourceAppType(StrEnum):
    AUTH_APP = "auth-app"
    PAYMENT_APP = "payment-app"
    ORDER_APP = "order-app"


class LogStatus(StrEnum):
    """
    Log severity and health status.

    NORMAL   -> logs look fine
    INFO     -> informational event
    WARNING  -> possible issue detected
    HIGH     -> major issue
    CRITICAL -> urgent/system-breaking issue
    """

    NORMAL = "normal"
    INFO = "info"
    WARNING = "warning"
    HIGH = "high"
    CRITICAL = "critical"
