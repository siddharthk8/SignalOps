import uuid
from io import BytesIO

import boto3
from fastapi.concurrency import run_in_threadpool
from PIL import Image, ImageOps
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.models.user import User
from app.db.repositories.user import UserRepository
from app.domains.auth.utils import DUMMY_HASH, verify_password


async def get_user(db: AsyncSession, id: uuid.UUID) -> User | None:
    user = await UserRepository(db).get_by_id(id)
    return user


async def authenticate_user(db: AsyncSession, id: uuid.UUID, password: str) -> bool:
    user = await get_user(db, id)
    if user is None:
        # Using a dummy hash to ensure authentication takes roughly the same time
        # whether or not the user exists, minimizing timing-based information leakage.
        verify_password(password, DUMMY_HASH)
        return False

    if not verify_password(password, user.password_hash):
        return False

    return True


# image utils
def process_profile_image(data: bytes) -> tuple[bytes, str]:
    with Image.open(BytesIO(data)) as real_file:
        image = ImageOps.exif_transpose(real_file)
        image = ImageOps.fit(image, (512, 512), method=Image.Resampling.LANCZOS)

        if image.mode in ("RGBA", "LA", "P"):
            image = image.convert("RGB")

        output = BytesIO()
        image.save(output, "JPEG", quality=85, optimize=True)
        output.seek(0)

    image_name = f"{uuid.uuid4().hex}.jpg"
    return output.read(), image_name


def _get_boto3_s3_client():
    return boto3.client(
        "s3",
        region_name=settings.s3_region,
        aws_access_key_id=(
            settings.aws_access_key_id.get_secret_value()
            if settings.aws_access_key_id
            else None
        ),
        aws_secret_access_key=(
            settings.aws_secret_access_key.get_secret_value()
            if settings.aws_secret_access_key
            else None
        ),
    )


def _save_profile_image(image_bytes: bytes, path: str):
    s3_client = _get_boto3_s3_client()
    s3_client.upload_fileobj(
        BytesIO(image_bytes),
        settings.s3_bucket_name,
        path,
        ExtraArgs={
            "ContentType": "image/jpeg"
        },  # This ensures the browser displays the image instead of downloading it.
    )


def _remove_profile_image(path: str):
    s3_client = _get_boto3_s3_client()
    s3_client.delete_object(
        Bucket=settings.s3_bucket_name,
        Key=path,
    )


async def save_profile_image(image_bytes: bytes, image_name: str):
    path = f"profile_images/{image_name}"
    await run_in_threadpool(
        _save_profile_image,
        image_bytes,
        path,
    )


async def remove_profile_image(image_name: str):
    if image_name is None:
        return

    path = f"profile_images/{image_name}"
    await run_in_threadpool(
        _remove_profile_image,
        path,
    )


def mask_email_for_log(email: str) -> str:
    local, domain = email.split("@", 1)

    if len(local) <= 2:
        masked_local = local[0] + "*"
    else:
        masked_local = local[:2] + "*" * (len(local) - 2)

    return f"{masked_local}@{domain}"
