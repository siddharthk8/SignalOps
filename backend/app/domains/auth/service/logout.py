from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.refresh_token import RefreshTokenRepository
from app.domains.auth.schemas import RefreshTokenRequest
from app.domains.auth.utils import get_refresh_token_hash


async def revoke_refresh_token(
    refresh_token_data: RefreshTokenRequest, db: AsyncSession
):
    refresh_token = refresh_token_data.refresh_token
    token_hash = get_refresh_token_hash(refresh_token)

    rt_repo = RefreshTokenRepository(db)
    await rt_repo.revoke_refresh_token(token_hash)
    await db.commit()
