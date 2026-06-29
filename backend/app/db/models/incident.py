from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.core import Base
from app.db.models.signal_incident import SignalIncident
from app.enums.common import Severity
from app.enums.incident import IncidentStatus, IncidentType

if TYPE_CHECKING:
    from app.db.models.ai_analysis import AIAnalysis
    from app.db.models.user import User


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    incident_type: Mapped[IncidentType] = mapped_column(
        Enum(
            IncidentType,
            values_callable=lambda enum: [e.value for e in enum],
        ),
        nullable=False,
    )
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[IncidentStatus] = mapped_column(
        Enum(
            IncidentStatus,
            values_callable=lambda enum: [e.value for e in enum],
        ),
        nullable=False,
    )
    severity: Mapped[Severity] = mapped_column(
        Enum(
            Severity,
            values_callable=lambda enum: [e.value for e in enum],
        ),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    summary: Mapped[str] = mapped_column(String(1000), nullable=False)

    # FK
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # relationships
    user: Mapped[User] = relationship(
        "User", passive_deletes=True, back_populates="incidents"
    )
    ai_analysis: Mapped[AIAnalysis] = relationship(
        "AIAnalysis", passive_deletes=True, back_populates="incident"
    )
    signal_incidents: Mapped[list[SignalIncident]] = relationship(
        "SignalIncident", passive_deletes=True, back_populates="incident"
    )

    # datetime
    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    __table_args__ = (
        CheckConstraint(
            "confidence >= 0.0 and confidence <= 1.0",
            name="incident_confidence_range_check",
        ),
    )
