from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import auth_logger
from app.domains.user.dependencies import CurrentUser
from app.domains.user.schemas import UserPrivate, UserUpdate


async def update_current_user(
    data: UserUpdate, current_user: CurrentUser, db: AsyncSession
) -> UserPrivate:
    has_changes = False
    if data.first_name is not None:
        has_changes = True
        current_user.first_name = data.first_name

    if data.last_name is not None:
        has_changes = True
        current_user.last_name = data.last_name

    if has_changes is False:
        auth_logger.warning(
            "User profile update rejected: no fields provided. user_id=%s",
            current_user.id,
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update.",
        )

    response = UserPrivate.model_validate(current_user)

    await db.commit()
    return response
