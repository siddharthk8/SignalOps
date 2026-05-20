from app.enums.common import Severity
from app.enums.event import GenericEventType


def get_generic_severity(event_type: GenericEventType) -> Severity:

    if event_type in {
        GenericEventType.PRIVILEGE_ESCALATION_ATTEMPT,
        GenericEventType.BRUTE_FORCE_DETECTED,
        GenericEventType.SERVICE_UNAVAILABLE,
        GenericEventType.INTERNAL_SERVICE_ERROR,
        GenericEventType.DATABASE_ERROR,
        GenericEventType.STORAGE_LIMIT_EXCEEDED,
        GenericEventType.DATA_INCONSISTENCY,
        GenericEventType.STATE_MISMATCH,
        GenericEventType.DEADLOCK_DETECTED,
        GenericEventType.DEAD_LETTER_QUEUE_EVENT,
        GenericEventType.EVENT_INGESTION_FAILED,
    }:
        return Severity.CRITICAL

    if event_type in {
        GenericEventType.SECURITY_THREAT_DETECTED,
        GenericEventType.MALICIOUS_PAYLOAD_DETECTED,
        GenericEventType.SUSPICIOUS_ACTIVITY,
        GenericEventType.REQUEST_BLOCKED,
        GenericEventType.AUTHORIZATION_FAILED,
        GenericEventType.UNAUTHORIZED_REQUEST,
        GenericEventType.SERVICE_TIMEOUT,
        GenericEventType.DEPENDENCY_FAILURE,
        GenericEventType.DOWNSTREAM_SERVICE_FAILURE,
        GenericEventType.CONFIGURATION_ERROR,
        GenericEventType.CONNECTION_FAILED,
        GenericEventType.DATABASE_TIMEOUT,
        GenericEventType.QUERY_FAILED,
        GenericEventType.MESSAGE_RETRY_EXCEEDED,
        GenericEventType.EVENT_PROCESSING_TIMEOUT,
        GenericEventType.MESSAGE_PROCESSING_FAILED,
        GenericEventType.RETRY_EXHAUSTED,
        GenericEventType.RECONCILIATION_MISMATCH,
        GenericEventType.IDEMPOTENCY_CONFLICT,
        GenericEventType.CACHE_CONNECTION_FAILED,
        GenericEventType.CACHE_WRITE_FAILED,
        GenericEventType.FILE_UPLOAD_FAILED,
        GenericEventType.HEALTH_CHECK_FAILED,
        GenericEventType.METRIC_THRESHOLD_EXCEEDED,
    }:
        return Severity.HIGH

    if event_type in {
        GenericEventType.RATE_LIMIT_EXCEEDED,
        GenericEventType.THROTTLING_APPLIED,
        GenericEventType.REQUEST_REJECTED,
        GenericEventType.INVALID_REQUEST,
        GenericEventType.INVALID_INPUT,
        GenericEventType.MALFORMED_PAYLOAD,
        GenericEventType.VALIDATION_FAILED,
        GenericEventType.SCHEMA_VALIDATION_FAILED,
        GenericEventType.RESOURCE_NOT_FOUND,
        GenericEventType.RESOURCE_CONFLICT,
        GenericEventType.RESOURCE_LOCKED,
        GenericEventType.FILE_NOT_FOUND,
        GenericEventType.NETWORK_ERROR,
        GenericEventType.DNS_RESOLUTION_FAILED,
        GenericEventType.CONNECTION_TIMEOUT,
        GenericEventType.REQUEST_TIMEOUT,
        GenericEventType.TRANSACTION_ROLLBACK,
        GenericEventType.LOGGING_FAILURE,
        GenericEventType.TRACING_ERROR,
        GenericEventType.EVENT_PARSE_FAILED,
        GenericEventType.EVENT_DROPPED,
        GenericEventType.CACHE_MISS,
        GenericEventType.CIRCUIT_BREAKER_OPEN,
        GenericEventType.FALLBACK_TRIGGERED,
        GenericEventType.OPERATION_FAILED,
    }:
        return Severity.MEDIUM

    return Severity.LOW
