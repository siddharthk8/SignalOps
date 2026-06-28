from datetime import datetime
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.password_reset_token import PasswordResetToken


class PasswordResetTokenRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_token_hash(self, token_hash: str) -> PasswordResetToken | None:
        query = await self.db.execute(
            select(PasswordResetToken)
            .options(selectinload(PasswordResetToken.user))
            .where(PasswordResetToken.token_hash == token_hash)
        )
        result = query.scalar_one_or_none()
        return result

    async def get_by_user_id(self, user_id: UUID) -> PasswordResetToken | None:
        query = await self.db.execute(
            select(PasswordResetToken)
            .options(selectinload(PasswordResetToken.user))
            .where(PasswordResetToken.user_id == user_id)
        )
        result = query.scalar_one_or_none()
        return result

    async def save(self, token_hash: str, user_id: UUID, expires_at: datetime):
        self.db.add(
            PasswordResetToken(
                token_hash=token_hash, user_id=user_id, expires_at=expires_at
            )
        )
        await self.db.flush()

    async def remove_all(self, user_id: UUID):
        await self.db.execute(
            delete(PasswordResetToken).where(PasswordResetToken.user_id == user_id)
        )
