from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, Enum, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.core import Base
from app.enums.signal import AllSignalType

if TYPE_CHECKING:
    from app.db.models.batch import Batch
    from app.db.models.entity import Entity
    from app.db.models.event_signal import EventSignal


class Signal(Base):
    __tablename__ = "signals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    signal_type: Mapped[
        StrEnum  # unable to use AllSignalType here because "AllSignalType" is dynamically created, instead of statically typed.
    ] = mapped_column(
        Enum(
            AllSignalType,
            values_callable=lambda enum: [e.value for e in enum],
        ),
        nullable=False,
    )
    confidence: Mapped[float] = mapped_column(Float, nullable=False)

    # FK
    entity_id: Mapped[int | None] = mapped_column(
        ForeignKey("entities.id", ondelete="CASCADE"), nullable=True
    )
    batch_id: Mapped[int] = mapped_column(
        ForeignKey("batches.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # relationships
    batch: Mapped[Batch] = relationship(
        "Batch", passive_deletes=True, back_populates="signals"
    )
    entity: Mapped[Entity | None] = relationship(
        "Entity", passive_deletes=True, back_populates="signals"
    )
    event_signals: Mapped[list[EventSignal]] = relationship(
        "EventSignal", passive_deletes=True, back_populates="signal"
    )

    # datetime
    triggered_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    __table_args__ = (
        CheckConstraint(
            "confidence >= 0.0 and confidence <= 1.0",
            name="signal_confidence_range_check",
        ),
    )
