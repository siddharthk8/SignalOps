from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.user import UserRepository
from app.domains.auth.utils import (
    get_password_hash,
)
from app.domains.user.schemas import UserCreate, UserPrivate


async def create_user(data: UserCreate, db: AsyncSession) -> UserPrivate:
    user_repo = UserRepository(db)

    if await user_repo.check_exists_by_email(data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists.",
        )

    await user_repo.save_user(data, password_hash=get_password_hash(data.password))
    response = UserPrivate(
        **data.model_dump(exclude={"password"}), is_active=True, profile_image_path=None
    )

    await db.commit()
    return response
