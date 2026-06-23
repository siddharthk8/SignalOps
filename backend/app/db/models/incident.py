from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

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
from app.enums.common import Severity
from app.enums.incident import IncidentStatus, IncidentType

if TYPE_CHECKING:
    from app.db.models.ai_analysis import AIAnalysis
    from app.db.models.signal import Signal


class Incident(Base):
    __tablename__ = "incident"

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
    ai_analysis_id: Mapped[int] = mapped_column(
        ForeignKey("ai_analysis.id"), nullable=True, index=True
    )

    # relationships
    signals: Mapped[list[Signal]] = relationship("Signal", back_populates="incident")
    ai_analysis: Mapped[AIAnalysis] = relationship(
        "AIAnalysis", back_populates="incidents"
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
    resolved_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    __table_args__ = (
        CheckConstraint(
            "confidence >= 0.0 and confidence <= 1.0",
            name="incident_confidence_range_check",
        ),
    )
