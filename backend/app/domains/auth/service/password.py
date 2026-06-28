from datetime import UTC, datetime, timedelta

from fastapi import BackgroundTasks, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.repositories.password_reset_token import PasswordResetTokenRepository
from app.db.repositories.refresh_token import RefreshTokenRepository
from app.db.repositories.user import UserRepository
from app.domains.auth.schemas import ForgotPasswordRequest, ResetPasswordRequest
from app.domains.auth.utils import (
    generate_reset_token,
    get_password_hash,
    get_reset_token_hash,
    send_reset_password_email,
)


async def forgot_password(
    data: ForgotPasswordRequest, background_tasks: BackgroundTasks, db: AsyncSession
):
    user_repo = UserRepository(db)
    password_reset_token_repo = PasswordResetTokenRepository(db)

    user = await user_repo.get_by_email(data.email)
    if user:
        await password_reset_token_repo.remove_all(user.id)

        token = generate_reset_token()
        token_hash = get_reset_token_hash(token)
        expires_at = datetime.now(UTC) + timedelta(
            minutes=settings.reset_token_expire_minutes,
        )

        await password_reset_token_repo.save(
            token_hash=token_hash, user_id=user.id, expires_at=expires_at
        )
        await db.commit()
        await db.refresh(user)

        background_tasks.add_task(
            send_reset_password_email,
            token=token,
            first_name=user.first_name,
            to_email=user.email,
        )

    return {
        "message": "If an account exists with this email address, you will receive password reset instructions shortly."
    }


async def reset_password(data: ResetPasswordRequest, db: AsyncSession):
    token_hash = get_reset_token_hash(data.token)

    user_repo = UserRepository(db)
    password_reset_token_repo = PasswordResetTokenRepository(db)
    password_reset_orm = await password_reset_token_repo.get_by_token_hash(token_hash)

    if not password_reset_orm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token.",
        )

    expires = password_reset_orm.expires_at
    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=UTC)

    if expires < datetime.now(UTC):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token.",  # Keeping the response generic to improve safety.
        )

    if token_hash == password_reset_orm.token_hash:
        current_user = password_reset_orm.user
        current_user.password_hash = get_password_hash(data.new_password)

        # to invalidate previous tokens
        await user_repo.increment_token_version(current_user)

        rt_repo = RefreshTokenRepository(db)
        await rt_repo.revoke_refresh_tokens(current_user)

        await db.commit()

    return {
        "message": "Your password has been reset successfully. You can now log in using your new password.",
    }
