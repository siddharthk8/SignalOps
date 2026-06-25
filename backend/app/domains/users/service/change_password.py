from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db.repositories.password_reset_token import PasswordResetTokenRepository
from app.db.repositories.refresh_token import RefreshTokenRepository
from app.db.repositories.user import UserRepository
from app.domains.auth.utils import get_password_hash, verify_password
from app.domains.users.dependencies import CurrentUser
from app.domains.users.schemas import UserPasswordChange


async def change_password(
    data: UserPasswordChange, current_user: CurrentUser, db: Session
):
    user_repo = UserRepository(db)

    if not verify_password(data.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect.",
        )

    current_user.password_hash = get_password_hash(data.new_password)

    # to invalidate previous tokens
    user_repo.increment_token_version(current_user)

    rt_repo = RefreshTokenRepository(db)
    rt_repo.revoke_refresh_tokens(current_user)

    # If a user initiates a password reset but later remembers their existing password
    # and successfully changes it through the normal flow, any pending reset tokens
    # should be invalidated to prevent reuse or confusion.
    password_reset_token_repo = PasswordResetTokenRepository(db)
    password_reset_token_repo.delete_all(current_user.id)

    db.commit()
