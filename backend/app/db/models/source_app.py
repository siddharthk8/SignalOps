from __future__ import (
    annotations,  # delays evaluation of type hints, prevents circular import issues
)

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.core import Base
from app.enums.common import SourceAppType

if TYPE_CHECKING:  # this block runs only for type checkers (mypy/IDE), not at runtime
    from app.db.models.batch import Batch
    from app.db.models.user import (
        User,  # imported only for typing, avoids runtime circular imports
    )


class SourceApp(Base):
    __tablename__ = "source_app"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    app_type: Mapped[SourceAppType] = mapped_column(
        Enum(
            SourceAppType,
            values_callable=lambda enum: [
                e.value for e in enum
            ],  # "values_callable" Stores enum values (e.g. "auth-app") instead of member names (e.g. "AUTH_APP")
        ),
        nullable=False,
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    # FK
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user.id"),
        nullable=False,
        index=True,  # FKs are not indexed by default. So we need to index imp FKs.
    )

    # relationships (these works only at ORM/Python level)
    creator: Mapped[User] = relationship("User", back_populates="source_apps")
    batches: Mapped[list[Batch]] = relationship("Batch", back_populates="source_app")

    # datetime
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
