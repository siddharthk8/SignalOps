from collections import defaultdict
from collections.abc import Callable
from datetime import datetime, timedelta

# TIME WINDOW
from typing import Any, cast

from app.schemas.event import SemanticEvent


def get_sorted_ts_events(
    events: list[SemanticEvent],
    functional_check: Callable[[SemanticEvent], bool] | None = None,
) -> list[SemanticEvent]:
    events_with_ts = [e for e in events if e.timestamp is not None]

    # step-1 -> apply functional_check FIRST
    if functional_check is not None:
        events_with_ts = [e for e in events_with_ts if functional_check(e)]

    sorted_ts_events = sorted(
        events_with_ts,
        key=lambda e: cast(datetime, e.timestamp),
    )

    return sorted_ts_events


def threshold_window(
    *,
    events: list[SemanticEvent],
    minutes: int,
    threshold: int,
    functional_check: Callable[[SemanticEvent], bool] | None = None,
) -> list[SemanticEvent]:

    # Events might already be sorted but we can't rely on assumption.
    sorted_ts_events = get_sorted_ts_events(events, functional_check)

    # sliding window
    left = 0
    for right in range(len(sorted_ts_events)):
        cutoff = cast(datetime, sorted_ts_events[right].timestamp) - timedelta(
            minutes=minutes
        )

        while cast(datetime, sorted_ts_events[left].timestamp) < cutoff:
            left += 1

        event_count = right - left + 1  # The number of events currently in the window
        if event_count >= threshold:
            return sorted_ts_events[left : right + 1]

    return []


def events_in_last_minutes(
    events: list[SemanticEvent],
    minutes: int,
) -> list[SemanticEvent]:
    """Return events inside a rolling window."""

    if not events:
        return []

    timestamps = [e.timestamp for e in events if e.timestamp is not None]
    if not timestamps:
        return []

    cutoff = max(timestamps) - timedelta(minutes=minutes)
    return [e for e in events if e.timestamp is not None and e.timestamp >= cutoff]


def events_between(
    events: list[SemanticEvent],
    start: datetime,
    end: datetime,
) -> list[SemanticEvent]:
    return [e for e in events if e.timestamp and start <= e.timestamp <= end]


# GROUPING
def group_by_user(events: list[SemanticEvent]) -> dict[str, list[SemanticEvent]]:
    events_by_user: dict[str, list[SemanticEvent]] = defaultdict(list)

    # group by users
    for event in events:
        user = event.entity.user
        if not user:
            continue

        events_by_user[user].append(event)

    return events_by_user


def group_by_user_and_filter(
    events: list[SemanticEvent],
    *,
    functional_check: Callable[[SemanticEvent], bool],
) -> dict[str, list[SemanticEvent]]:
    filtered_events: list[SemanticEvent] = []

    # group by users
    for event in events:
        if functional_check(event) is False:
            continue

        filtered_events.append(event)

    events_by_user = group_by_user(filtered_events)
    return events_by_user


# SEQUENCE DETECTION
def contains_sequence(
    events: list[SemanticEvent],
    sequence: list[Any],
) -> bool:
    """
    Example:

    LOGIN_FAIL
    LOGIN_FAIL
    LOGIN_SUCCESS
    PASSWORD_CHANGE

    sequence:
    LOGIN_SUCCESS
    PASSWORD_CHANGE
    """

    event_types = [
        (e.event_type)
        for e in sorted(
            events,
            key=lambda x: x.timestamp or datetime.min,
        )
    ]

    i = 0
    for event_type in event_types:
        if event_type == sequence[i]:
            i += 1

            if i == len(sequence):
                return True

    return False
