import random
from datetime import UTC, datetime, timedelta

from fastapi import BackgroundTasks, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.logger import auth_logger
from app.db.repositories.email_suppression import EmailSuppressionRepository
from app.db.repositories.otp import OtpRepository
from app.db.repositories.user import UserRepository
from app.domains.auth.utils import (
    get_password_hash,
)
from app.domains.user.schemas import UserCreate, UserCreationOTPStep, UserPrivate
from app.domains.user.utils import (
    get_otp_hash,
    is_registration_email_valid,
    mask_email_for_log,
    send_registration_otp_email,
    verify_otp,
)


async def create_user_otp(
    data: UserCreationOTPStep, background_tasks: BackgroundTasks, db: AsyncSession
):
    user_repo = UserRepository(db)
    email_suppression_repo = EmailSuppressionRepository(db)

    if await email_suppression_repo.get_with_email(data.email) is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User registration is not allowed for this email address.",
        )

    if not is_registration_email_valid(data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please use an email address from a recognized email provider.",
        )

    if await user_repo.check_exists_by_email(data.email):
        auth_logger.warning(
            "User registration rejected (email already exists). email=%s",
            mask_email_for_log(data.email),
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists.",
        )

    otp_repo = OtpRepository(db)
    otp_object = await otp_repo.get_otp_object_by_email(data.email)

    if otp_object is not None and otp_object.count >= 3:
        auth_logger.warning(
            "Max Registration OTP attempts excceded. email=%s",
            mask_email_for_log(data.email),
        )
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many OTP requests. Please contact support.",
        )

    otp = str(random.randint(100000, 999999))
    otp_hash = get_otp_hash(otp)
    expires_at = datetime.now(UTC) + timedelta(minutes=settings.otp_expire_minutes)

    if otp_object is None:
        await otp_repo.create(otp_hash, data.email, expires_at)
    else:
        await otp_repo.update_otp_hash(otp_hash, data.email, expires_at)

    # send mail.
    background_tasks.add_task(
        send_registration_otp_email,
        otp=otp,
        first_name=data.first_name,
        to_email=data.email,
    )

    await db.commit()


async def verify_create_user_otp(data: UserCreate, db: AsyncSession) -> UserPrivate:
    user_repo = UserRepository(db)

    if await user_repo.check_exists_by_email(data.email):
        auth_logger.warning(
            "User registration rejected (email already exists). email=%s",
            mask_email_for_log(data.email),
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists.",
        )

    otp_repo = OtpRepository(db)
    otp_object = await otp_repo.get_otp_object_by_email(data.email)

    if otp_object is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Something went wrong.",
        )

    if verify_otp(
        data.otp, otp_object.otp_hash
    ) and otp_object.expires_at > datetime.now(UTC):
        await user_repo.save_user(data, password_hash=get_password_hash(data.password))
        response = UserPrivate(
            **data.model_dump(exclude={"password", "otp"}),
            is_active=True,
            profile_image_path=None,
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or incorrect OTP.",
        )

    await db.commit()
    return response
