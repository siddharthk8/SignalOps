from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, Enum, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.core import Base
from app.enums.common import Severity
from app.enums.event import AllEventType, ParsingMethodType

if TYPE_CHECKING:
    from app.db.models.batch import Batch
    from app.db.models.entity import Entity
    from app.db.models.signal import Signal


class Event(Base):
    __tablename__ = "event"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_type: Mapped[
        StrEnum  # unable to use AllEventType here because "AllEventType" is dynamically created, instead of statically typed.
    ] = mapped_column(
        Enum(
            AllEventType,
            values_callable=lambda enum: [e.value for e in enum],
        ),
        nullable=False,
    )
    parsing_method: Mapped[ParsingMethodType] = mapped_column(
        Enum(
            ParsingMethodType,
            values_callable=lambda enum: [e.value for e in enum],
        ),
        nullable=False,
    )
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    severity: Mapped[Severity] = mapped_column(
        Enum(
            Severity,
            values_callable=lambda enum: [e.value for e in enum],
        ),
        nullable=False,
    )

    # FK
    log_id: Mapped[int] = mapped_column(
        ForeignKey("log.id"), nullable=False, index=True
    )
    batch_id: Mapped[int] = mapped_column(
        ForeignKey("batch.id"), nullable=False, index=True
    )
    signal_id: Mapped[int] = mapped_column(
        ForeignKey("signal.id"), nullable=True, index=True
    )
    entity_id: Mapped[int] = mapped_column(
        ForeignKey("entity.id"), nullable=True, index=True
    )

    # relationships
    batch: Mapped[Batch] = relationship("Batch", back_populates="events")
    log: Mapped[Batch] = relationship("Log", back_populates="event")
    entity: Mapped[Entity] = relationship("Entity", back_populates="event")
    signal: Mapped[Signal] = relationship("Signal", back_populates="events")

    # datetime
    timestamp: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    __table_args__ = (
        CheckConstraint(
            "confidence >= 0.0 and confidence <= 1.0",
            name="event_confidence_range_check",
        ),
    )
