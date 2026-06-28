from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.user import UserRepository
from app.domains.user.dependencies import CurrentUser


async def delete_current_user(current_user: CurrentUser, db: AsyncSession):
    user_repo = UserRepository(db)
    await user_repo.remove_user(current_user)
    await db.commit()
