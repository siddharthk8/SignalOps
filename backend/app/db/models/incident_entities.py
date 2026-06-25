from __future__ import annotations

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.core import Base


class IncidentEntities(Base):
    __tablename__ = "incident_entities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # FK
    entity_id: Mapped[int] = mapped_column(
        ForeignKey("entity.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    incident_id: Mapped[int] = mapped_column(
        ForeignKey("incident.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
