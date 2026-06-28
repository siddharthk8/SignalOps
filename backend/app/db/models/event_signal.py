from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.core import Base

if TYPE_CHECKING:
    from app.db.models.signal import Signal


class EventSignal(Base):
    __tablename__ = "event_signals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # FK
    event_id: Mapped[int] = mapped_column(
        ForeignKey("events.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    signal_id: Mapped[int] = mapped_column(
        ForeignKey("signals.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # relationships
    signal: Mapped[Signal] = relationship(
        "Signal", passive_deletes=True, back_populates="event_signals"
    )
