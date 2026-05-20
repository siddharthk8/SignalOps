from app.engine.parsing.parsers.payment.patterns import PAYMENT_EVENT_PATTERNS
from app.engine.parsing.parsers.shared.generic_severity import get_generic_severity
from app.enums.common import Severity
from app.enums.event import GenericEventType, PaymentEventType
from app.schemas.event import SemanticEvent
from app.schemas.log import LogField

from ...base import BaseParser


class PaymentParser(BaseParser):
    @staticmethod
    def get_severity(event_type: PaymentEventType | GenericEventType) -> Severity:

        if isinstance(event_type, GenericEventType):
            return get_generic_severity(event_type=event_type)

        if event_type in {
            PaymentEventType.PAYMENT_FRAUD_SUSPECTED,
            PaymentEventType.HIGH_RISK_TRANSACTION,
            PaymentEventType.CHARGEBACK_INITIATED,
            PaymentEventType.IDEMPOTENCY_CONFLICT,
            PaymentEventType.TRANSACTION_INCONSISTENCY,
            PaymentEventType.RECONCILIATION_MISMATCH,
            PaymentEventType.WEBHOOK_SIGNATURE_INVALID,
        }:
            return Severity.CRITICAL

        if event_type in {
            PaymentEventType.PAYMENT_FAILED,
            PaymentEventType.PAYMENT_DECLINED,
            PaymentEventType.PAYMENT_TIMEOUT,
            PaymentEventType.PAYMENT_GATEWAY_ERROR,
            PaymentEventType.PAYMENT_PROVIDER_UNAVAILABLE,
            PaymentEventType.BANKING_NETWORK_ERROR,
            PaymentEventType.RECURRING_PAYMENT_FAILED,
            PaymentEventType.INVOICE_PAYMENT_FAILED,
            PaymentEventType.CARD_VERIFICATION_FAILED,
            PaymentEventType.PAYMENT_METHOD_REJECTED,
            PaymentEventType.INVALID_PAYMENT_METHOD,
            PaymentEventType.INSUFFICIENT_FUNDS,
            PaymentEventType.VELOCITY_LIMIT_EXCEEDED,
            PaymentEventType.SUSPICIOUS_PAYMENT_PATTERN,
            PaymentEventType.GEOLOCATION_MISMATCH,
            PaymentEventType.PAYMENT_REVERSED,
        }:
            return Severity.HIGH

        if event_type in {
            PaymentEventType.PAYMENT_CANCELLED,
            PaymentEventType.REFUND_INITIATED,
            PaymentEventType.REFUND_FAILED,
            PaymentEventType.REFUND_CANCELLED,
            PaymentEventType.PARTIAL_REFUND_ISSUED,
            PaymentEventType.PAYMENT_AUTHORIZED,
            PaymentEventType.PAYMENT_CAPTURED,
            PaymentEventType.PAYMENT_INITIATED,
            PaymentEventType.PAYMENT_METHOD_EXPIRED,
            PaymentEventType.CURRENCY_MISMATCH,
            PaymentEventType.SUBSCRIPTION_CANCELLED,
            PaymentEventType.RECURRING_PAYMENT_FAILED,
        }:
            return Severity.MEDIUM

        return Severity.LOW

    def parse(self, log: LogField, position: int) -> SemanticEvent | None:
        return self.global_parse(
            log=log, position=position, PATTERNS=PAYMENT_EVENT_PATTERNS
        )
