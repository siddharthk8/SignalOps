from __future__ import (
    annotations,  # delays evaluation of type hints, prevents circular import issues
)

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.core import Base
from app.enums.common import SourceAppType

if TYPE_CHECKING:  # this block runs only for type checkers (mypy/IDE), not at runtime
    from app.db.models.batch import Batch
    from app.db.models.user import (
        User,  # imported only for typing, avoids runtime circular imports
    )


class SourceApp(Base):
    __tablename__ = "source_apps"

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

    access_key: Mapped[str | None] = mapped_column(
        String(255), nullable=True, default=None, index=True
    )
    secret_access_key_hash: Mapped[str | None] = mapped_column(
        String(255), nullable=True, default=None
    )

    # FK
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,  # FKs are not indexed by default. So we need to index imp FKs.
    )

    # relationships (these works only at ORM/Python level)
    user: Mapped[User] = relationship(
        "User", passive_deletes=True, back_populates="source_apps"
    )
    batches: Mapped[list[Batch]] = relationship(
        "Batch", passive_deletes=True, back_populates="source_app"
    )

    # datetime
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint(
            """
            (access_key IS NULL AND secret_access_key_hash IS NULL)
            OR
            (access_key IS NOT NULL AND secret_access_key_hash IS NOT NULL)
            """,
            name="ck_source_apps_tokens_both_present_or_absent",
        ),
    )
