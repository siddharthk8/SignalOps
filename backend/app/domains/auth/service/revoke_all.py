from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.refresh_token import RefreshTokenRepository
from app.db.repositories.user import UserRepository
from app.domains.users.dependencies import CurrentUser


async def revoke_all_refresh_tokens(current_user: CurrentUser, db: AsyncSession):
    user_repo = UserRepository(db)
    # to invalidate previous tokens
    await user_repo.increment_token_version(current_user)

    rt_repo = RefreshTokenRepository(db)
    await rt_repo.revoke_refresh_tokens(current_user)
    await db.commit()
