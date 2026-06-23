from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, Enum, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.core import Base
from app.enums.signal import AllSignalType

if TYPE_CHECKING:
    from app.db.models.entity import Entity
    from app.db.models.event import Event
    from app.db.models.incident import Incident


class Signal(Base):
    __tablename__ = "signal"

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
    entity_id: Mapped[int] = mapped_column(ForeignKey("entity.id"), nullable=True)
    incident_id: Mapped[int] = mapped_column(
        ForeignKey("incident.id"), nullable=True, index=True
    )

    # relationships
    events: Mapped[list[Event]] = relationship("Event", back_populates="signal")
    entity: Mapped[Entity] = relationship("Entity", back_populates="signals")
    incident: Mapped[Incident] = relationship("Incident", back_populates="signals")

    # datetime
    triggered_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    __table_args__ = (
        CheckConstraint(
            "confidence >= 0.0 and confidence <= 1.0",
            name="signal_confidence_range_check",
        ),
    )
