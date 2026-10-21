from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.oauth_account import OAuthAccount


class OAuthAccountRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_for_google(self, user_id: UUID, sub_id: str):
        oauth_account = OAuthAccount(
            user_id=user_id,
            provider="google",
            provider_user_id=sub_id,
        )
        self.db.add(oauth_account)
        await self.db.flush()

    async def get_google_oauth_by_provider_user_id(
        self, sub_id: str
    ) -> OAuthAccount | None:
        query = await self.db.execute(
            select(OAuthAccount).where(
                OAuthAccount.provider == "google",
                OAuthAccount.provider_user_id == sub_id,
            )
        )
        return query.scalar_one_or_none()

    async def filter_by_user_id(self, user_id: UUID) -> Sequence[OAuthAccount]:
        query = await self.db.execute(
            select(OAuthAccount).where(OAuthAccount.user_id == user_id)
        )
        return query.scalars().all()
