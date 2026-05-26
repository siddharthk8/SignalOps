from abc import ABC, abstractmethod
from typing import Any

from app.engine.parsing import utility
from app.engine.parsing.parsers.shared.generic_patterns import GENERIC_EVENT_PATTERNS
from app.enums.common import Severity, SourceAppType
from app.schemas.entity import Entity
from app.schemas.event import SemanticEvent
from app.schemas.log import (
    JSONIncomingLog,
    LogField,
)
from app.shared.constants import ALL_EVENT_TYPES


class BaseParser(ABC):
    @abstractmethod
    def get_severity(self, event_type: ALL_EVENT_TYPES) -> Severity:
        pass

    def clamp_confidence(self, value: float) -> float:
        """
        We use this to be assure that the confidence remains within valid limit range.
        """

        return round(max(0.0, min(1.0, value)), 2)

    def proximity_score(self, tokens: list[str], key_tokens: list[str]) -> float:
        """
        - Checks how close important tokens appear to each other in the message.
        - Closer words = higher score.
        - This is useful because related words appearing together usually indicate stronger relevance.
        """

        # Find positions/indexes of important tokens
        positions = [i for (i, token) in enumerate(tokens) if token in key_tokens]

        # If fewer than 2 keywords exist, proximity cannot be measured well
        if len(positions) < 2:
            return 0.2

        # Distance between farthest matching tokens
        spread = max(positions) - min(positions)

        # Smaller spread = higher score
        return self.clamp_confidence(1.0 - (spread / len(tokens)))

    def phrase_bonus(self, message: str, signature: dict) -> float:
        """
        Gives extra score if complete phrases exist in the message.
        This improves confidence because exact phrases are stronger signals than individual words.
        """

        score = 0.0

        for token_group in signature["tokens"]:
            if token_group in message:
                score += 0.4

        # Prevent bonus from becoming too large
        return min(score, 0.8)

    def matches_pattern(self, tokens: list[str], pattern: list[str]) -> bool:
        """
        Token-based matching is used instead of raw substring search to ensure word-level accuracy.
        This avoids false matches (e.g., "dev" in "devasted") and improves reliability for noisy log data.
        """

        for word in pattern:
            if word not in tokens:
                return False
        return True

    def match_score(self, patterns: list[list[str]], tokens: list[str]) -> float:
        ms = 0.0

        for pattern in patterns:
            total_weight = len(pattern)
            current_weight = 0

            for p in pattern:
                if p in tokens:
                    current_weight += 1

            ms = max(ms, current_weight / total_weight)

        return self.clamp_confidence(ms)

    def generic_parser(
        self, candidates: list[Any], tokens: list[str], log: LogField
    ) -> None:
        for event_type, patterns in GENERIC_EVENT_PATTERNS.items():
            match_score = self.match_score(patterns, tokens)
            if match_score < 0.3:
                continue

            proximity = self.proximity_score(
                tokens, [token for p in patterns for token in p]
            )

            confidence = match_score * 0.70 + proximity * 0.30

            # if event_type == GenericEventType.RESOURCE_NOT_FOUND:
            #     print("\n RESOURCE_NOT_FOUND")
            #     print("match_score : ", match_score)
            #     print("proximity : ", proximity)
            #     print("confidence : ", confidence)

            # if event_type == GenericEventType.DATABASE_TIMEOUT:
            #     print("\n DATABASE_TIMEOUT")
            #     print("match_score : ", match_score)
            #     print("proximity : ", proximity)
            #     print("confidence : ", confidence)

            if confidence >= 0.6:
                candidates.append((event_type, confidence))

    def global_parse(
        self,
        log: LogField,
        position: int,
        PATTERNS: dict[Any, list[list[str]]],
        source_app: SourceAppType,
    ) -> SemanticEvent | None:
        if isinstance(log, JSONIncomingLog):
            message = log.message or ""
        else:
            message = log or ""

        message = utility.normalize_log_for_tokens(message)
        tokens = message.split()
        candidates: list[tuple[Any, float]] = []

        for event_type, patterns in PATTERNS.items():
            match_score = self.match_score(patterns, tokens)
            if match_score < 0.3:
                continue

            proximity = self.proximity_score(
                tokens, [token for p in patterns for token in p]
            )

            confidence = match_score * 0.70 + proximity * 0.30

            if confidence >= 0.6:
                candidates.append((event_type, confidence))

        self.generic_parser(candidates=candidates, tokens=tokens, log=log)

        if not candidates:
            return None

        best_event, best_conf = max(candidates, key=lambda x: x[1])

        return SemanticEvent(
            sequence=position,
            source_app=source_app,
            event_type=best_event,
            severity=self.get_severity(best_event),
            confidence=self.clamp_confidence(best_conf),
            timestamp=utility.get_timestamp(log),
            raw_log=log,
            entity=Entity(
                ip_address=utility.get_ip_address(log),
                user=utility.get_user(log),
                email=utility.get_email(log),
                session_id=utility.get_session_id(log),
                request_id=utility.get_request_id(log),
                token_id=utility.get_token_id(log),
            ),
        )
