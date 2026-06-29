from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, CheckConstraint, DateTime, Integer, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.config import settings
from app.db.core import Base

if TYPE_CHECKING:
    from app.db.models.incident import Incident
    from app.db.models.password_reset_token import PasswordResetToken
    from app.db.models.refresh_token import RefreshToken
    from app.db.models.source_app import SourceApp


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )
    password_hash: Mapped[str] = mapped_column(String(200), nullable=False)
    first_name: Mapped[str] = mapped_column(String(60), nullable=False)
    last_name: Mapped[str] = mapped_column(String(80), nullable=False)
    profile_image: Mapped[str | None] = mapped_column(
        String(200), nullable=True, default=None
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Increment it to invalidate all previously issued JWTs.
    token_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    # relationships
    incidents: Mapped[list[Incident]] = relationship(
        "Incident", passive_deletes=True, back_populates="user"
    )
    source_apps: Mapped[list[SourceApp]] = relationship(
        "SourceApp", passive_deletes=True, back_populates="user"
    )
    refresh_tokens: Mapped[list[RefreshToken]] = relationship(
        "RefreshToken", passive_deletes=True, back_populates="user"
    )
    password_reset_tokens: Mapped[list[PasswordResetToken]] = relationship(
        "PasswordResetToken",
        passive_deletes=True,
        back_populates="user",
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
        CheckConstraint("token_version > 0", name="user_token_version_positive"),
    )

    @property
    def profile_image_path(self):
        if self.profile_image:
            return f"https://{settings.s3_bucket_name}.s3.{settings.s3_region}.amazonaws.com/profile_images/{self.profile_image}"
        return None
