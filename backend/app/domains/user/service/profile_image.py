from botocore.exceptions import ClientError
from fastapi import HTTPException, UploadFile, status
from fastapi.concurrency import run_in_threadpool
from PIL import UnidentifiedImageError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.logger import auth_logger
from app.domains.user.dependencies import CurrentUser
from app.domains.user.schemas import UserPrivate
from app.domains.user.utils import (
    process_profile_image,
    remove_profile_image,
    save_profile_image,
)


async def upload_profile_image(
    file: UploadFile, current_user: CurrentUser, db: AsyncSession
):
    file_bytes = await file.read()

    # This is more reliable method to check file size, than .size
    if len(file_bytes) > settings.max_upload_size_bytes:
        auth_logger.warning(
            "Profile image upload rejected: file too large. user_id=%s file_size_bytes=%d max_size_bytes=%d",
            current_user.id,
            file_bytes,
            settings.max_upload_size_bytes,
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum size is {settings.max_upload_size_bytes // (1024 * 1024)}MB",
        )

    # Process the file
    try:
        image_bytes, image_name = await run_in_threadpool(
            process_profile_image, file_bytes
        )
    except UnidentifiedImageError as err:
        auth_logger.warning(
            "Profile image upload rejected: invalid file type. user_id=%s content_type=%s filename=%s",
            current_user.id,
            file.content_type,
            file.filename,
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image file. Please upload a valid image (JPEG, PNG, GIF, WebP).",
        ) from err

    # Upload image to S3 bucket
    try:
        await save_profile_image(image_bytes, image_name)
    except ClientError as err:
        auth_logger.error(
            "Image upload failed. user_id=%s filename=%s content_type=%s",
            current_user.id,
            file.filename,
            file.content_type,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload image. Please try again.",
        ) from err

    # Updat the user
    previous_profile_image = current_user.profile_image

    current_user.profile_image = image_name
    await db.commit()
    await db.refresh(current_user)

    if previous_profile_image is not None:
        # Delete previous profile image from S3 bucket
        try:
            await remove_profile_image(previous_profile_image)
        except ClientError:
            # Ignore S3 errors: image is already removed from DB; cleanup can be retried later
            auth_logger.warning(
                "Profile image cleanup failed: S3 delete operation failed. user_id=%s image=%s",
                current_user.id,
                previous_profile_image,
            )
    return UserPrivate.model_validate(current_user)


async def delete_profile_image(current_user: CurrentUser, db: AsyncSession):
    previous_profile_image = current_user.profile_image

    if previous_profile_image is None:
        auth_logger.warning(
            "Profile image deletion rejected: image not found. user_id=%s",
            current_user.id,
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No profile picture to delete.",
        )

    current_user.profile_image = None
    await db.commit()

    # Delete image from S3 bucket
    try:
        await remove_profile_image(previous_profile_image)
    except ClientError:
        # Ignore S3 errors: image is already removed from DB; cleanup can be retried later
        pass
