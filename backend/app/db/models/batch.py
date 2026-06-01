from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.core import Base

if TYPE_CHECKING:
    from app.db.models.event import Event
    from app.db.models.log import Log
    from app.db.models.source_app import SourceApp


class Batch(Base):
    __tablename__ = "batch"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # FK
    source_app_id: Mapped[int] = mapped_column(
        ForeignKey("source_app.id"), nullable=False, index=True
    )

    # relationships
    source_app: Mapped[SourceApp] = relationship("SourceApp", back_populates="batches")
    logs: Mapped[list[Log]] = relationship("Log", back_populates="batch")
    events: Mapped[list[Event]] = relationship("Event", back_populates="batch")

    # datetime
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
