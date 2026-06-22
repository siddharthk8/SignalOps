from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db.repositories.user import UserRepository
from app.domains.auth.utils import (
    get_password_hash,
)
from app.domains.users.schemas import UserCreate, UserPrivate


async def create_user(user: UserCreate, db: Session) -> UserPrivate:
    user_repo = UserRepository(db)

    if user_repo.check_exists_by_email(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists.",
        )

    user_repo.create_user(user, password_hash=get_password_hash(user.password))
    new_user = UserPrivate(**user.model_dump(exclude={"password"}), is_active=True)

    db.commit()
    return new_user
