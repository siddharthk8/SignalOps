from app.engine.parsing.parsers.order.patterns import ORDER_EVENT_PATTERNS
from app.engine.parsing.parsers.shared.generic_severity import get_generic_severity
from app.enums.common import Severity, SourceAppType
from app.enums.event import GenericEventType, OrderEventType
from app.schemas.event import SemanticEvent
from app.schemas.log import PersistedLog

from ...base import BaseParser


class OrderParser(BaseParser):
    @staticmethod
    def get_severity(event_type: OrderEventType | GenericEventType) -> Severity:

        if isinstance(event_type, GenericEventType):
            return get_generic_severity(event_type=event_type)

        if event_type in {
            OrderEventType.INVALID_ORDER_STATE,
            OrderEventType.ORDER_STATE_INCONSISTENCY,
            OrderEventType.PAYMENT_ORDER_MISMATCH,
            OrderEventType.HIGH_RISK_ORDER,
        }:
            return Severity.CRITICAL

        if event_type in {
            OrderEventType.ORDER_PROCESSING_FAILED,
            OrderEventType.ORDER_VALIDATION_FAILED,
            OrderEventType.ORDER_FULFILLMENT_FAILED,
            OrderEventType.DELIVERY_FAILED,
            OrderEventType.ORDER_PAYMENT_FAILED,
            OrderEventType.INVENTORY_RESERVATION_FAILED,
            OrderEventType.INVENTORY_UNAVAILABLE,
            OrderEventType.STOCK_LEVEL_CRITICAL,
            OrderEventType.ORDER_WORKFLOW_TIMEOUT,
            OrderEventType.ORDER_ROLLBACK_INITIATED,
            OrderEventType.ORDER_COMPENSATION_TRIGGERED,
            OrderEventType.SUSPICIOUS_ORDER_PATTERN,
            OrderEventType.BULK_ORDER_ANOMALY,
            OrderEventType.DUPLICATE_ORDER_DETECTED,
            OrderEventType.ORDER_CANCEL_FAILED,
            OrderEventType.ORDER_CREATION_FAILED,
            OrderEventType.INVALID_ORDER_REQUEST,
            OrderEventType.DELIVERY_DELAY_DETECTED,
        }:
            return Severity.HIGH

        if event_type in {
            OrderEventType.ORDER_EXPIRED,
            OrderEventType.ORDER_CANCELLED,
            OrderEventType.ORDER_NOT_FOUND,
            OrderEventType.REFUND_ORDER_INITIATED,
            OrderEventType.ORDER_PAYMENT_PENDING,
            OrderEventType.ORDER_PROCESSING_STARTED,
            OrderEventType.ORDER_FULFILLMENT_STARTED,
            OrderEventType.INVENTORY_RESERVED,
            OrderEventType.INVENTORY_RELEASED,
        }:
            return Severity.MEDIUM

        return Severity.LOW

    def parse(self, log: PersistedLog, sequence: int) -> SemanticEvent | None:
        return self.global_parser(
            log=log,
            sequence=sequence,
            PATTERNS=ORDER_EVENT_PATTERNS,
            source_app=SourceAppType.ORDER_APP,
        )
