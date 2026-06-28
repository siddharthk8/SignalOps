from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.core import Base

if TYPE_CHECKING:
    from app.db.models.incident import Incident


class SignalIncident(Base):
    __tablename__ = "signal_incidents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # FK
    signal_id: Mapped[int] = mapped_column(
        ForeignKey("signals.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    incident_id: Mapped[int] = mapped_column(
        ForeignKey("incidents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # relationship
    incident: Mapped[Incident] = relationship(
        "Incident", passive_deletes=True, back_populates="signal_incidents"
    )
