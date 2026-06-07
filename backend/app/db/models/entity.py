from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.core import Base

if TYPE_CHECKING:
    from app.db.models.event import Event
    from app.db.models.signal import Signal


class Entity(Base):
    __tablename__ = "entity"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user: Mapped[datetime | None] = mapped_column(String, nullable=True)
    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    session_id: Mapped[str] = mapped_column(String(60), nullable=True)
    token_id: Mapped[str | None] = mapped_column(String(60), nullable=True)
    request_id: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # relationships
    event: Mapped[Event] = relationship("Event", back_populates="entity")
    signals: Mapped[list[Signal]] = relationship("Signal", back_populates="entity")
