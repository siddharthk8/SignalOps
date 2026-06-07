from enum import StrEnum


class ParsingMethodType(StrEnum):
    AI = "ai"
    HEURISTIC = "heuristic"


class AuthEventType(StrEnum):
    # Authentication
    LOGIN_ATTEMPT = "login_attempt"
    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILED = "login_failed"
    INVALID_CREDENTIALS = "invalid_credentials"
    USER_NOT_FOUND = "user_not_found"
    ACCOUNT_LOCKED = "account_locked"
    ACCOUNT_DISABLED = "account_disabled"
    ACCOUNT_SUSPENDED = "account_suspended"

    # Session Lifecycle
    SESSION_CREATED = "session_created"
    SESSION_EXPIRED = "session_expired"
    SESSION_INVALID = "session_invalid"
    SESSION_TERMINATED = "session_terminated"

    # Logout
    LOGOUT = "logout"

    # Token Lifecycle
    TOKEN_ISSUED = "token_issued"
    TOKEN_EXPIRED = "token_expired"
    TOKEN_INVALID = "token_invalid"
    TOKEN_REVOKED = "token_revoked"
    TOKEN_REFRESH_SUCCESS = "token_refresh_success"
    TOKEN_REFRESH_FAILED = "token_refresh_failed"

    # MFA
    MFA_REQUIRED = "mfa_required"
    MFA_CHALLENGE_SENT = "mfa_challenge_sent"
    MFA_SUCCESS = "mfa_success"
    MFA_FAILED = "mfa_failed"
    MFA_BYPASS_ATTEMPT = "mfa_bypass_attempt"

    # Password Management
    PASSWORD_CHANGE_SUCCESS = "password_change_success"
    PASSWORD_CHANGE_FAILED = "password_change_failed"
    PASSWORD_RESET_REQUESTED = "password_reset_requested"
    PASSWORD_RESET_SUCCESS = "password_reset_success"
    PASSWORD_RESET_FAILED = "password_reset_failed"
    PASSWORD_POLICY_VIOLATION = "password_policy_violation"

    # Identity Lifecycle
    USER_REGISTERED = "user_registered"
    USER_DELETED = "user_deleted"
    EMAIL_VERIFICATION_SENT = "email_verification_sent"
    EMAIL_VERIFIED = "email_verified"

    # Auth Intelligence
    SUSPICIOUS_LOGIN = "suspicious_login"
    IMPOSSIBLE_TRAVEL_DETECTED = "impossible_travel_detected"
    ACCOUNT_TAKEOVER_SUSPECTED = "account_takeover_suspected"
    SESSION_HIJACK_SUSPECTED = "session_hijack_suspected"

    # Auth Infrastructure
    AUTH_SERVICE_ERROR = "auth_service_error"
    AUTH_PROVIDER_UNAVAILABLE = "auth_provider_unavailable"
    OAUTH_ERROR = "oauth_error"
    SSO_FAILURE = "sso_failure"
    LDAP_AUTH_FAILURE = "ldap_auth_failure"


class PaymentEventType(StrEnum):
    # Payment Lifecycle
    PAYMENT_INITIATED = "payment_initiated"
    PAYMENT_AUTHORIZED = "payment_authorized"
    PAYMENT_CAPTURED = "payment_captured"
    PAYMENT_SUCCESS = "payment_success"
    PAYMENT_FAILED = "payment_failed"
    PAYMENT_DECLINED = "payment_declined"
    PAYMENT_CANCELLED = "payment_cancelled"
    PAYMENT_REVERSED = "payment_reversed"
    PAYMENT_TIMEOUT = "payment_timeout"

    # Refund Lifecycle
    REFUND_INITIATED = "refund_initiated"
    REFUND_SUCCESS = "refund_success"
    REFUND_FAILED = "refund_failed"
    REFUND_CANCELLED = "refund_cancelled"
    PARTIAL_REFUND_ISSUED = "partial_refund_issued"

    # Transaction Integrity
    DUPLICATE_TRANSACTION = "duplicate_transaction"
    IDEMPOTENCY_CONFLICT = "idempotency_conflict"
    TRANSACTION_INCONSISTENCY = "transaction_inconsistency"
    RECONCILIATION_MISMATCH = "reconciliation_mismatch"

    # Payment Method / Validation
    INVALID_PAYMENT_METHOD = "invalid_payment_method"
    PAYMENT_METHOD_EXPIRED = "payment_method_expired"
    PAYMENT_METHOD_REJECTED = "payment_method_rejected"
    CARD_VERIFICATION_FAILED = "card_verification_failed"
    INSUFFICIENT_FUNDS = "insufficient_funds"
    CURRENCY_MISMATCH = "currency_mismatch"

    # Fraud / Risk Intelligence
    PAYMENT_FRAUD_SUSPECTED = "payment_fraud_suspected"
    HIGH_RISK_TRANSACTION = "high_risk_transaction"
    CHARGEBACK_INITIATED = "chargeback_initiated"
    CHARGEBACK_RECEIVED = "chargeback_received"
    VELOCITY_LIMIT_EXCEEDED = "velocity_limit_exceeded"
    SUSPICIOUS_PAYMENT_PATTERN = "suspicious_payment_pattern"
    GEOLOCATION_MISMATCH = "geolocation_mismatch"

    # Gateway / Provider / Infra
    PAYMENT_GATEWAY_ERROR = "payment_gateway_error"
    PAYMENT_PROVIDER_UNAVAILABLE = "payment_provider_unavailable"
    BANKING_NETWORK_ERROR = "banking_network_error"
    PAYMENT_WEBHOOK_FAILED = "payment_webhook_failed"
    WEBHOOK_SIGNATURE_INVALID = "webhook_signature_invalid"

    # Subscription / Billing
    SUBSCRIPTION_CREATED = "subscription_created"
    SUBSCRIPTION_RENEWED = "subscription_renewed"
    SUBSCRIPTION_CANCELLED = "subscription_cancelled"
    RECURRING_PAYMENT_FAILED = "recurring_payment_failed"
    INVOICE_GENERATED = "invoice_generated"
    INVOICE_PAYMENT_FAILED = "invoice_payment_failed"

    # New
    REFUND_REQUESTED = "refund_requested"
    PAYMENT_RETRY = "payment_retry"


class OrderEventType(StrEnum):
    # Order Lifecycle
    ORDER_CREATED = "order_created"
    ORDER_UPDATED = "order_updated"
    ORDER_CONFIRMED = "order_confirmed"
    ORDER_COMPLETED = "order_completed"
    ORDER_CANCELLED = "order_cancelled"
    ORDER_EXPIRED = "order_expired"

    # Order Processing
    ORDER_PROCESSING_STARTED = "order_processing_started"
    ORDER_PROCESSING_FAILED = "order_processing_failed"
    ORDER_VALIDATION_FAILED = "order_validation_failed"
    INVALID_ORDER_STATE = "invalid_order_state"
    DUPLICATE_ORDER_DETECTED = "duplicate_order_detected"

    # Fulfillment / Shipping
    ORDER_FULFILLMENT_STARTED = "order_fulfillment_started"
    ORDER_FULFILLMENT_FAILED = "order_fulfillment_failed"
    ORDER_SHIPPED = "order_shipped"
    ORDER_DELIVERED = "order_delivered"
    DELIVERY_DELAY_DETECTED = "delivery_delay_detected"
    DELIVERY_FAILED = "delivery_failed"

    # Inventory Coordination
    INVENTORY_RESERVED = "inventory_reserved"
    INVENTORY_RESERVATION_FAILED = "inventory_reservation_failed"
    INVENTORY_UNAVAILABLE = "inventory_unavailable"
    INVENTORY_RELEASED = "inventory_released"
    STOCK_LEVEL_CRITICAL = "stock_level_critical"

    # Payment Coordination
    ORDER_PAYMENT_PENDING = "order_payment_pending"
    ORDER_PAYMENT_CONFIRMED = "order_payment_confirmed"
    ORDER_PAYMENT_FAILED = "order_payment_failed"
    PAYMENT_ORDER_MISMATCH = "payment_order_mismatch"
    REFUND_ORDER_INITIATED = "refund_order_initiated"

    # Customer / Request Issues
    ORDER_NOT_FOUND = "order_not_found"
    ORDER_CREATION_FAILED = "order_creation_failed"
    ORDER_CANCEL_FAILED = "order_cancel_failed"
    INVALID_ORDER_REQUEST = "invalid_order_request"

    # Distributed Workflow / Saga
    ORDER_WORKFLOW_TIMEOUT = "order_workflow_timeout"
    ORDER_STATE_INCONSISTENCY = "order_state_inconsistency"
    ORDER_ROLLBACK_INITIATED = "order_rollback_initiated"
    ORDER_COMPENSATION_TRIGGERED = "order_compensation_triggered"

    # Fraud / Risk
    SUSPICIOUS_ORDER_PATTERN = "suspicious_order_pattern"
    HIGH_RISK_ORDER = "high_risk_order"
    BULK_ORDER_ANOMALY = "bulk_order_anomaly"

    # new
    CHECKOUT_STARTED = "checkout_started"
    CART_ABANDONED = "cart_abandoned"


class GenericEventType(StrEnum):
    # Access / Authorization
    ACCESS_DENIED = "access_denied"
    PERMISSION_DENIED = "permission_denied"
    AUTHORIZATION_FAILED = "authorization_failed"
    UNAUTHORIZED_REQUEST = "unauthorized_request"

    # Security / Threat Intelligence
    SECURITY_THREAT_DETECTED = "security_threat_detected"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    BRUTE_FORCE_DETECTED = "brute_force_detected"
    PRIVILEGE_ESCALATION_ATTEMPT = "privilege_escalation_attempt"
    MALICIOUS_PAYLOAD_DETECTED = "malicious_payload_detected"
    ABNORMAL_TRAFFIC_PATTERN = "abnormal_traffic_pattern"
    IP_BLOCKED = "ip_blocked"

    # Traffic / API Protection
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    THROTTLING_APPLIED = "throttling_applied"
    REQUEST_BLOCKED = "request_blocked"
    REQUEST_REJECTED = "request_rejected"

    # Validation / Input Errors
    INVALID_REQUEST = "invalid_request"
    INVALID_INPUT = "invalid_input"
    MALFORMED_PAYLOAD = "malformed_payload"
    VALIDATION_FAILED = "validation_failed"
    SCHEMA_VALIDATION_FAILED = "schema_validation_failed"

    # Resource State
    RESOURCE_NOT_FOUND = "resource_not_found"
    RESOURCE_CONFLICT = "resource_conflict"
    RESOURCE_LOCKED = "resource_locked"
    RESOURCE_EXHAUSTED = "resource_exhausted"
    RESOURCE_ALREADY_EXISTS = "resource_already_exists"

    # Infrastructure / Service Health
    SERVICE_UNAVAILABLE = "service_unavailable"
    SERVICE_TIMEOUT = "service_timeout"
    INTERNAL_SERVICE_ERROR = "internal_service_error"
    DEPENDENCY_FAILURE = "dependency_failure"
    DOWNSTREAM_SERVICE_FAILURE = "downstream_service_failure"
    CONFIGURATION_ERROR = "configuration_error"
    CONNECTION_FAILED = "connection_failed"

    # Network / Communication
    NETWORK_ERROR = "network_error"
    DNS_RESOLUTION_FAILED = "dns_resolution_failed"
    CONNECTION_TIMEOUT = "connection_timeout"
    REQUEST_TIMEOUT = "request_timeout"

    # Resilience / Retry / Circuit Breaker
    RETRY_ATTEMPTED = "retry_attempted"
    RETRY_SUCCEEDED = "retry_succeeded"
    RETRY_EXHAUSTED = "retry_exhausted"
    BACKOFF_APPLIED = "backoff_applied"

    CIRCUIT_BREAKER_OPEN = "circuit_breaker_open"
    CIRCUIT_BREAKER_HALF_OPEN = "circuit_breaker_half_open"
    CIRCUIT_BREAKER_CLOSED = "circuit_breaker_closed"

    FALLBACK_TRIGGERED = "fallback_triggered"

    # Data / State Integrity
    DATA_INCONSISTENCY = "data_inconsistency"
    STATE_MISMATCH = "state_mismatch"
    DUPLICATE_EVENT_DETECTED = "duplicate_event_detected"
    IDEMPOTENCY_CONFLICT = "idempotency_conflict"
    RECONCILIATION_MISMATCH = "reconciliation_mismatch"

    # Queue / Async Processing
    MESSAGE_PROCESSING_FAILED = "message_processing_failed"
    MESSAGE_RETRY_EXCEEDED = "message_retry_exceeded"
    DEAD_LETTER_QUEUE_EVENT = "dead_letter_queue_event"
    EVENT_PROCESSING_TIMEOUT = "event_processing_timeout"

    # Event Pipeline Integrity (SIGNALOPS CORE)
    EVENT_INGESTION_FAILED = "event_ingestion_failed"
    EVENT_PARSE_FAILED = "event_parse_failed"
    EVENT_DROPPED = "event_dropped"
    EVENT_DUPLICATE_SUPPRESSED = "event_duplicate_suppressed"

    # Database / Persistence
    DATABASE_ERROR = "database_error"
    DATABASE_TIMEOUT = "database_timeout"
    QUERY_FAILED = "query_failed"
    TRANSACTION_ROLLBACK = "transaction_rollback"
    DEADLOCK_DETECTED = "deadlock_detected"

    # Cache
    CACHE_MISS = "cache_miss"
    CACHE_WRITE_FAILED = "cache_write_failed"
    CACHE_CONNECTION_FAILED = "cache_connection_failed"

    # File / Storage
    FILE_UPLOAD_FAILED = "file_upload_failed"
    FILE_NOT_FOUND = "file_not_found"
    STORAGE_LIMIT_EXCEEDED = "storage_limit_exceeded"

    # Observability / Monitoring (IMPORTANT FOR AIOPS)
    HEALTH_CHECK_FAILED = "health_check_failed"
    HEALTH_CHECK_SUCCESS = "health_check_success"
    METRIC_THRESHOLD_EXCEEDED = "metric_threshold_exceeded"
    LOGGING_FAILURE = "logging_failure"
    TRACING_ERROR = "tracing_error"

    # Lifecycle / Generic Operations
    OPERATION_STARTED = "operation_started"
    OPERATION_COMPLETED = "operation_completed"
    OPERATION_FAILED = "operation_failed"
    OPERATION_CANCELLED = "operation_cancelled"

    # Fallback / Unknown
    OTHER = "other"
    UNKNOWN = "unknown"


AllEventType = StrEnum(
    "AllEventType",
    {
        **{e.name: e.value for e in AuthEventType},
        **{e.name: e.value for e in OrderEventType},
        **{e.name: e.value for e in PaymentEventType},
        **{e.name: e.value for e in GenericEventType},
    },
)
