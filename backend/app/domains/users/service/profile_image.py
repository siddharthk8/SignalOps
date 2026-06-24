from botocore.exceptions import ClientError
from fastapi import HTTPException, UploadFile, status
from fastapi.concurrency import run_in_threadpool
from PIL import UnidentifiedImageError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.domains.users.dependencies import CurrentUser
from app.domains.users.utils import (
    process_profile_image,
    remove_profile_image,
    save_profile_image,
)


async def upload_profile_image(
    file: UploadFile, current_user: CurrentUser, db: Session
):
    file_bytes = await file.read()

    # This is more reliable method to check file size, than .size
    if len(file_bytes) > settings.max_upload_size_bytes:
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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image file. Please upload a valid image (JPEG, PNG, GIF, WebP).",
        ) from err

    # Upload image to S3 bucket
    try:
        await save_profile_image(image_bytes, image_name)
    except ClientError as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload image. Please try again.",
        ) from err

    # Updat the user
    previous_profile_image = current_user.profile_image

    current_user.profile_image = image_name
    db.commit()
    db.refresh(current_user)

    if previous_profile_image is not None:
        # Delete previous profile image from S3 bucket
        try:
            await remove_profile_image(previous_profile_image)
        except ClientError:
            # Ignore S3 errors: image is already removed from DB; cleanup can be retried later
            pass

    return current_user


async def delete_profile_image(current_user: CurrentUser, db: Session):
    previous_profile_image = current_user.profile_image

    if previous_profile_image is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No profile picture to delete",
        )

    current_user.profile_image = None
    db.commit()

    # Delete image from S3 bucket
    try:
        await remove_profile_image(previous_profile_image)
    except ClientError:
        # Ignore S3 errors: image is already removed from DB; cleanup can be retried later
        pass
