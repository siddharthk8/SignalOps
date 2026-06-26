from datetime import UTC, datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.refresh_token import RefreshToken as ORMRefreshToken
from app.db.models.user import User
from app.domains.auth.schemas import RefreshToken


class RefreshTokenRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_refresh_token(self, refresh_token_obj: RefreshToken):
        self.db.add(ORMRefreshToken(**refresh_token_obj.model_dump()))
        await self.db.flush()

    async def revoke_refresh_tokens(self, user: User):
        await self.db.execute(
            update(ORMRefreshToken)
            .where(
                ORMRefreshToken.user_id == user.id,
                ORMRefreshToken.is_revoked.is_(False),
            )
            .values(is_revoked=True, revoked_at=datetime.now(UTC))
        )

    async def revoke_refresh_token(self, token_hash: str):
        await self.db.execute(
            update(ORMRefreshToken)
            .where(
                ORMRefreshToken.token_hash == token_hash,
                ORMRefreshToken.is_revoked.is_(False),
            )
            .values(is_revoked=True, revoked_at=datetime.now(UTC))
        )

    async def get_by_token_hash(self, token_hash: str) -> ORMRefreshToken | None:
        query = await self.db.execute(
            select(ORMRefreshToken)
            .options(selectinload(ORMRefreshToken.user))
            .where(
                ORMRefreshToken.token_hash == token_hash,
            )
        )
        result = query.scalar_one_or_none()
        return result
