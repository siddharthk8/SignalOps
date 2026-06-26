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
from app.enums.incident import IncidentType

if TYPE_CHECKING:
    from app.db.models.batch import Batch
    from app.db.models.incident import Incident


class AIAnalysis(Base):
    __tablename__ = "ai_analysis"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    summary: Mapped[str] = mapped_column(String(1000), nullable=False)
    root_cause: Mapped[str] = mapped_column(String(1000), nullable=False)
    business_impact: Mapped[str] = mapped_column(String(1000), nullable=False)
    recommendations: Mapped[str] = mapped_column(String(1000), nullable=False)

    severity: Mapped[Severity] = mapped_column(
        Enum(
            Severity,
            values_callable=lambda enum: [e.value for e in enum],
        ),
        nullable=False,
    )
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    incident_type: Mapped[IncidentType] = mapped_column(
        Enum(
            IncidentType,
            values_callable=lambda enum: [e.value for e in enum],
        ),
        nullable=False,
    )

    # FK
    batch_id: Mapped[int] = mapped_column(
        ForeignKey("batch.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # relationships
    incidents: Mapped[list[Incident]] = relationship(
        "Incident", passive_deletes=True, back_populates="ai_analysis"
    )
    batch: Mapped[Batch] = relationship(
        "Batch", passive_deletes=True, back_populates="ai_analyses"
    )

    # datetime
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint(
            "confidence >= 0.0 and confidence <= 1.0",
            name="ai_analysis_confidence_range_check",
        ),
    )
