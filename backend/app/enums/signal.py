from enum import StrEnum


class AuthSignalType(StrEnum):
    POSSIBLE_ACCOUNT_COMPROMISE = "possible_account_compromise"
    EXCESSIVE_AUTH_FAILURES = "excessive_auth_failures"
    SUSPICIOUS_SESSION_ACTIVITY = "suspicious_session_activity"
    TOKEN_ABUSE_PATTERN = "token_abuse_pattern"


class PaymentSignalType(StrEnum):
    PAYMENT_FAILURE_SPIKE = "payment_failure_spike"
    REFUND_ABUSE_PATTERN = "refund_abuse_pattern"
    PAYMENT_RETRY_STORM = "payment_retry_storm"


class OrderSignalType(StrEnum):
    CHECKOUT_ABANDONMENT_SURGE = "checkout_abandonment_surge"
    ORDER_CANCELLATION_SPIKE = "order_cancellation_spike"
    SUSPICIOUS_ORDER_ACTIVITY = "suspicious_order_activity"


class GenericSignalType(StrEnum):
    BRUTE_FORCE_ATTEMPT = "brute_force_attempt"
    CASCADING_SERVICE_FAILURE = "cascading_service_failure"
    DOWNSTREAM_SERVICE_DEGRADATION = "downstream_service_degradation"
    HIGH_ERROR_RATE_PATTERN = "high_error_rate_pattern"


AllSignalType = StrEnum(
    "AllSignalType",
    {
        **{s.name: s.value for s in AuthSignalType},
        **{s.name: s.value for s in PaymentSignalType},
        **{s.name: s.value for s in OrderSignalType},
        **{s.name: s.value for s in GenericSignalType},
    },
)
