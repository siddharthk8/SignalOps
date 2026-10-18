from datetime import UTC, datetime, timedelta

from fastapi import BackgroundTasks, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.logger import auth_logger
from app.db.repositories.email_suppression import EmailSuppressionRepository
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
    email_suppression_repo = EmailSuppressionRepository(db)

    if await email_suppression_repo.get_with_email(data.email) is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Password reset is not allowed for this email address.",
        )

    user = await user_repo.get_by_email(data.email)
    if user:
        last_prt_model = await password_reset_token_repo.get_by_user_id(user.id)
        if last_prt_model:
            created = last_prt_model.created_at
            if created.tzinfo is None:
                created = created.replace(tzinfo=UTC)

            remaining_secs = (
                created
                + timedelta(seconds=settings.password_reset_request_cooldown_seconds)
                - datetime.now(UTC)
            ).total_seconds()

            if remaining_secs > 0:
                auth_logger.warning(
                    "Password reset rate limit exceeded. user_id=%s retry_after=%ss",
                    user.id,
                    int(remaining_secs),
                )
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Too many password reset requests.",
                    headers={"Retry-After": str(int(remaining_secs))},
                )

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
