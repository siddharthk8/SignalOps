from abc import ABC, abstractmethod
from typing import Any

from app.engine.parsing import utils
from app.engine.parsing.parsers.shared.generic_patterns import GENERIC_EVENT_PATTERNS
from app.enums.common import Severity, SourceAppType
from app.enums.event import ParsingMethodType
from app.schemas.entity import Entity
from app.schemas.event import SemanticEvent
from app.schemas.log import (
    PersistedLog,
)
from app.shared.constants import ALL_EVENT_TYPES


class BaseParser(ABC):
    MIN_MATCH_SCORE = 0.30
    MIN_CONFIDENCE = 0.60

    @abstractmethod
    def get_severity(self, event_type: ALL_EVENT_TYPES) -> Severity:
        pass

    @abstractmethod
    def parse(self, log: PersistedLog, sequence: int) -> SemanticEvent | None:
        pass

    def clamp_confidence(self, value: float) -> float:
        """
        We use this to be assure that the confidence remains within valid limit range.
        """

        return round(max(0.0, min(1.0, value)), 2)

    def proximity_score(self, tokens: set[str], key_tokens: set[str]) -> float:
        """
        - Checks how close important tokens appear to each other in the message.
        - Closer words = higher score.
        - This is useful because related words appearing together usually indicate stronger relevance.
        """

        # Find positions/indexes of important tokens
        positions = [i for (i, token) in enumerate(tokens) if token in key_tokens]

        # If fewer than 2 keywords exist, proximity cannot be measured well
        if len(positions) <= 1:
            return 0.01

        # Distance between farthest matching tokens
        spread = max(positions) - min(positions)
        max_spread = len(tokens) - 1

        return 1.0 - (spread / max_spread)

    # NOTE: Future feature - not used yet
    # Keeping for upcoming release
    # def phrase_bonus(self, message: str, signature: dict) -> float:
    #     """
    #     Gives extra score if complete phrases exist in the message.
    #     This improves confidence because exact phrases are stronger signals than individual words.
    #     """
    #     score = 0.0
    #     for token_group in signature["tokens"]:
    #         if token_group in message:
    #             score += 0.4
    #     # Prevent bonus from becoming too large
    #     return min(score, 0.8)

    def match_score(self, patterns: list[list[str]], tokens: set[str]) -> float:
        """
        Token-based matching is used instead of raw substring search to ensure word-level accuracy.
        This avoids false matches (e.g., "dev" in "devasted") and improves reliability for noisy log data.
        """
        ms = 0.0

        for pattern in patterns:
            total_weight = len(pattern)
            current_weight = 0

            for p in pattern:
                if p in tokens:
                    current_weight += 1

            ms = max(ms, current_weight / total_weight)

        return ms

    def generic_parser(
        self, candidates: list[Any], tokens: set[str], log: PersistedLog
    ) -> None:
        for event_type, patterns in GENERIC_EVENT_PATTERNS.items():
            match_score = self.match_score(patterns, tokens)
            if match_score < self.MIN_MATCH_SCORE:
                continue

            proximity = self.proximity_score(
                tokens,
                {token for pattern in patterns for token in pattern},
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

            if confidence >= self.MIN_CONFIDENCE:
                candidates.append((event_type, confidence))

    def global_parser(
        self,
        log: PersistedLog,
        sequence: int,
        PATTERNS: dict[Any, list[list[str]]],
        source_app: SourceAppType,
    ) -> SemanticEvent | None:
        message = log.message

        message = utils.normalize_log_for_tokens(message)
        tokens = set(message.split())  # using set reduces time complexity
        candidates: list[tuple[Any, float]] = []

        for event_type, patterns in PATTERNS.items():
            match_score = self.match_score(patterns, tokens)
            if match_score < self.MIN_MATCH_SCORE:
                continue

            proximity = self.proximity_score(
                tokens, {token for pattern in patterns for token in pattern}
            )

            confidence = match_score * 0.70 + proximity * 0.30

            if confidence >= self.MIN_CONFIDENCE:
                candidates.append((event_type, confidence))

        self.generic_parser(candidates=candidates, tokens=tokens, log=log)

        if not candidates:
            return None

        best_event, best_conf = max(candidates, key=lambda x: x[1])

        return SemanticEvent(
            sequence=sequence,
            source_app=source_app,
            parsing_method=ParsingMethodType.HEURISTIC,
            event_type=best_event,
            severity=self.get_severity(best_event),
            confidence=self.clamp_confidence(best_conf),
            timestamp=utils.get_timestamp(log),
            persisted_log=log,
            entity=Entity(
                ip_address=utils.get_ip_address(log),
                user=utils.get_user(log),
                email=utils.get_email(log),
                session_id=utils.get_session_id(log),
                request_id=utils.get_request_id(log),
                token_id=utils.get_token_id(log),
            ),
        )
