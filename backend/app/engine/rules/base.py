from abc import ABC, abstractmethod

from app.schemas.event import SemanticEvent
from app.schemas.signal import Signal


class BaseRule(ABC):
    @abstractmethod
    def evaluate(self, events: list[SemanticEvent]) -> list[Signal]:
        """
        Takes normalized events and returns signals.
        """
        pass
