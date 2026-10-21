from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    UniqueConstraint,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.core import Base

if TYPE_CHECKING:
    from app.db.models.user import User


class OAuthAccount(Base):
    __tablename__ = "oauth_accounts"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Example: "google"
    provider: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    # Google's stable subject identifier ("sub"), not the email.
    # FK
    provider_user_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # FK
    user: Mapped[User] = relationship(
        "User",
        back_populates="oauth_accounts",
    )

    # datetime
    created_at: Mapped[datetime] = mapped_column(
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

    __table_args__ = (
        UniqueConstraint(
            "provider",
            "provider_user_id",
            name="uq_oauth_accounts_provider_user",
        ),
    )
