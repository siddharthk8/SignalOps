from datetime import UTC, datetime

from app.engine.rules.base import BaseRule
from app.engine.rules.utility import (
    contains_sequence,
    get_sorted_ts_events,
    group_by_user,
    threshold_window,
)
from app.enums.common import Severity
from app.enums.event import OrderEventType
from app.enums.rule import OrderSignalType
from app.schemas.event import SemanticEvent
from app.schemas.signal import Signal


class OrderRule(BaseRule):
    ORDER_FAILURE_THRESHOLD = 5
    CANCELLATION_THRESHOLD = 10
    CHECKOUT_ABANDON_THRESHOLD = 10
    RAPID_ORDER_THRESHOLD = 5

    def evaluate(self, events: list[SemanticEvent]) -> list[Signal]:
        signals: list[Signal] = []

        signals.extend(self._detect_checkout_abandonment_surge(events))
        signals.extend(self._detect_order_cancellation_spike(events))
        signals.extend(self._detect_suspicious_order_activity(events))

        return signals

    def _detect_checkout_abandonment_surge(
        self,
        events: list[SemanticEvent],
    ) -> list[Signal]:
        signals: list[Signal] = []

        sorted_ts_events = get_sorted_ts_events(events=events)
        events_by_user = group_by_user(sorted_ts_events)

        abandonment_pattern = [
            OrderEventType.CHECKOUT_STARTED,
            OrderEventType.CART_ABANDONED,
        ]

        for user_events in events_by_user.values():
            if not contains_sequence(user_events, abandonment_pattern):
                continue

            signals.append(
                Signal(
                    signal_type=OrderSignalType.CHECKOUT_ABANDONMENT_SURGE,
                    severity=Severity.MEDIUM,
                    confidence=0.80,
                    source_app=user_events[0].source_app,
                    entity=user_events[0].entity,
                    supporting_events=[e.sequence for e in user_events],
                    metadata={
                        "pattern": [str(x) for x in abandonment_pattern],
                    },
                    triggered_at=datetime.now(UTC),
                )
            )

        return signals

    def _detect_order_cancellation_spike(
        self,
        events: list[SemanticEvent],
    ) -> list[Signal]:
        signals: list[Signal] = []

        CANCEL_EVENTS = {
            OrderEventType.ORDER_CANCELLED,
        }

        events_by_user = group_by_user(events=events)

        for user_events in events_by_user.values():
            window = threshold_window(
                events=user_events,
                minutes=10,
                threshold=self.CANCELLATION_THRESHOLD,
                functional_check=lambda e: e.event_type in CANCEL_EVENTS,
            )

            if len(window) == 0:
                continue

            signals.append(
                Signal(
                    signal_type=OrderSignalType.ORDER_CANCELLATION_SPIKE,
                    severity=Severity.HIGH,
                    confidence=0.90,
                    source_app=window[0].source_app,
                    entity=window[0].entity,
                    supporting_events=[e.sequence for e in window],
                    metadata={
                        "cancellation_count": len(window),
                        "window_minutes": 10,
                    },
                    triggered_at=datetime.now(UTC),
                )
            )

        return signals

    def _detect_suspicious_order_activity(
        self,
        events: list[SemanticEvent],
    ) -> list[Signal]:
        signals: list[Signal] = []

        events_by_user = group_by_user(events=events)

        for user_events in events_by_user.values():
            window_events = threshold_window(
                events=user_events,
                minutes=2,
                threshold=self.RAPID_ORDER_THRESHOLD,
                functional_check=lambda e: e.event_type == OrderEventType.ORDER_CREATED,
            )

            if not window_events:
                continue

            signals.append(
                Signal(
                    signal_type=OrderSignalType.SUSPICIOUS_ORDER_ACTIVITY,
                    severity=Severity.HIGH,
                    confidence=0.85,
                    source_app=window_events[0].source_app,
                    entity=window_events[0].entity,
                    supporting_events=[e.sequence for e in window_events],
                    metadata={
                        "order_count": len(window_events),
                        "window_minutes": 2,
                    },
                    triggered_at=datetime.now(UTC),
                )
            )

        return signals
