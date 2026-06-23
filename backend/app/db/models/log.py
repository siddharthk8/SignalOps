from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import IPvAnyAddress
from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.core import Base
from app.enums.logs import LogLevel

if TYPE_CHECKING:
    from app.db.models.batch import Batch


class Log(Base):
    __tablename__ = "log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    message: Mapped[str] = mapped_column(String(500), nullable=False)
    level: Mapped[LogLevel | None] = mapped_column(
        Enum(
            LogLevel,
            values_callable=lambda enum: [e.value for e in enum],
        ),
        nullable=True,
    )
    user: Mapped[str | None] = mapped_column(String(100), nullable=True)
    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    ip_address: Mapped[IPvAnyAddress | None] = mapped_column(String(45), nullable=True)
    session_id: Mapped[str] = mapped_column(String(60), nullable=True)
    token_id: Mapped[str | None] = mapped_column(String(60), nullable=True)
    request_id: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # FK
    batch_id: Mapped[int] = mapped_column(
        ForeignKey("batch.id"), nullable=False, index=True
    )

    # relationships
    batch: Mapped[Batch] = relationship("Batch", back_populates="logs")
    event: Mapped[Batch] = relationship("Event", back_populates="log")

    # datetime
    timestamp: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
