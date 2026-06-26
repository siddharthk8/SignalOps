from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.users.dependencies import CurrentUser
from app.domains.users.schemas import UserPrivate, UserUpdate


async def update_current_user(
    data: UserUpdate, current_user: CurrentUser, db: AsyncSession
) -> UserPrivate:
    if data.first_name is not None:
        current_user.first_name = data.first_name

    if data.last_name is not None:
        current_user.last_name = data.last_name

    response = UserPrivate.model_validate(current_user)

    await db.commit()
    return response
