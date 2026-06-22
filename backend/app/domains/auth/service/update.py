from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.domains.auth.dependencies import CurrentUser
from app.domains.auth.schemas import UserPrivate, UserUpdate


async def update_current_user(
    data: UserUpdate, current_user: CurrentUser, db: Session
) -> UserPrivate:

    if data.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authorized to perform this action.",
        )

    if data.first_name is not None:
        current_user.first_name = data.first_name

    if data.last_name is not None:
        current_user.last_name = data.last_name

    new_user = UserPrivate.model_validate(current_user)

    db.commit()
    return new_user
