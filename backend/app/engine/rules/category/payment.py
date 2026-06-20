from datetime import UTC, datetime

from app.engine.rules.base import BaseRule
from app.engine.rules.utils import (
    events_in_last_minutes,
    group_by_user_and_filter,
    threshold_window,
)
from app.enums.event import PaymentEventType
from app.enums.signal import PaymentSignalType
from app.schemas.event import SemanticEvent
from app.schemas.signal import Signal


class PaymentRule(BaseRule):
    FAILURE_SPIKE_THRESHOLD = 10
    DECLINE_THRESHOLD = 5
    REFUND_THRESHOLD = 5
    RETRY_THRESHOLD = 8

    def evaluate(
        self,
        events: list[SemanticEvent],
    ) -> list[Signal]:
        signals: list[Signal] = []

        signals.extend(self._detect_payment_failure_spike(events))
        signals.extend(self._detect_refund_abuse(events))
        signals.extend(self._detect_payment_retry_storm(events))

        return signals

    def _detect_payment_failure_spike(
        self,
        events: list[SemanticEvent],
    ) -> list[Signal]:

        failed_events = threshold_window(
            events=events,
            threshold=self.FAILURE_SPIKE_THRESHOLD,
            minutes=5,
            functional_check=lambda e: e.event_type == PaymentEventType.PAYMENT_FAILED,
        )

        if len(failed_events) < self.FAILURE_SPIKE_THRESHOLD:
            return []

        return [
            Signal(
                signal_type=PaymentSignalType.PAYMENT_FAILURE_SPIKE,
                confidence=0.95,
                entity=failed_events[0].entity,
                supporting_events=failed_events,
                metadata={
                    "failure_count": len(failed_events),
                    "window_minutes": self.FAILURE_SPIKE_THRESHOLD,
                },
                triggered_at=datetime.now(UTC),
            )
        ]

    def _detect_refund_abuse(
        self,
        events: list[SemanticEvent],
    ) -> list[Signal]:
        signals: list[Signal] = []

        refunds_by_user = group_by_user_and_filter(
            events=events,
            functional_check=lambda event: (
                event.event_type == PaymentEventType.REFUND_REQUESTED
            ),
        )

        for user_events in refunds_by_user.values():
            if len(user_events) < self.REFUND_THRESHOLD:
                continue

            signals.append(
                Signal(
                    signal_type=PaymentSignalType.REFUND_ABUSE_PATTERN,
                    confidence=0.85,
                    entity=user_events[0].entity,
                    supporting_events=user_events,
                    metadata={
                        "refund_count": len(user_events),
                    },
                    triggered_at=datetime.now(UTC),
                )
            )

        return signals

    def _detect_payment_retry_storm(
        self,
        events: list[SemanticEvent],
    ) -> list[Signal]:
        signals: list[Signal] = []

        retries_by_user = group_by_user_and_filter(
            events=events,
            functional_check=lambda event: (
                event.event_type == PaymentEventType.PAYMENT_RETRY
            ),
        )

        # Apply rolling window per user
        for user_events in retries_by_user.values():
            window = events_in_last_minutes(user_events, minutes=2)

            if len(window) < self.RETRY_THRESHOLD:
                continue

            signals.append(
                Signal(
                    signal_type=PaymentSignalType.PAYMENT_RETRY_STORM,
                    confidence=0.90,
                    entity=window[0].entity,
                    supporting_events=window,
                    metadata={
                        "retry_count": len(window),
                        "window_minutes": self.RETRY_THRESHOLD,
                    },
                    triggered_at=datetime.now(UTC),
                )
            )

        return signals
