from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.password_reset_token import PasswordResetTokenRepository
from app.db.repositories.refresh_token import RefreshTokenRepository
from app.db.repositories.user import UserRepository
from app.domains.auth.utils import get_password_hash, verify_password
from app.domains.user.dependencies import CurrentUser
from app.domains.user.schemas import UserPasswordChange


async def change_password(
    data: UserPasswordChange, current_user: CurrentUser, db: AsyncSession
):
    user_repo = UserRepository(db)

    if not verify_password(data.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect.",
        )

    current_user.password_hash = get_password_hash(data.new_password)

    # to invalidate previous tokens
    await user_repo.increment_token_version(current_user)

    rt_repo = RefreshTokenRepository(db)
    await rt_repo.revoke_refresh_tokens(current_user)

    # If a user initiates a password reset but later remembers their existing password
    # and successfully changes it through the normal flow, any pending reset tokens
    # should be invalidated to prevent reuse or confusion.
    password_reset_token_repo = PasswordResetTokenRepository(db)
    await password_reset_token_repo.remove_all(current_user.id)

    await db.commit()
