import uuid
from io import BytesIO

import boto3
from fastapi.concurrency import run_in_threadpool
from fastapi.templating import Jinja2Templates
from PIL import Image, ImageOps
from pwdlib import PasswordHash
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.models.user import User
from app.db.repositories.user import UserRepository
from app.domains.auth.utils import DUMMY_HASH, get_boto3_ses_client, verify_password

password_hash = PasswordHash.recommended()


def verify_otp(plain_otp: str, hashed_otp: str) -> bool:
    return password_hash.verify(plain_otp, hashed_otp)


def get_otp_hash(plain_otp: str) -> str:
    return password_hash.hash(plain_otp)


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
    path = f"profile-images/{image_name}"
    await run_in_threadpool(
        _save_profile_image,
        image_bytes,
        path,
    )


async def remove_profile_image(image_name: str):
    if image_name is None:
        return

    path = f"profile-images/{image_name}"
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


# email
ALLOWED_EMAIL_DOMAINS = {
    "gmail.com",
    "googlemail.com",
    "outlook.com",
    "hotmail.com",
    "live.com",
    "yahoo.com",
    "yahoo.co.in",
    "icloud.com",
    "me.com",
    "proton.me",
    "protonmail.com",
}


def is_registration_email_valid(email: EmailStr) -> bool:
    normalized_email = str(email).strip().lower()
    domain = normalized_email.rsplit("@", 1)[-1]

    if domain in ALLOWED_EMAIL_DOMAINS:
        return True

    return False


templates = Jinja2Templates(directory="templates")


async def send_registration_otp_email(
    *,
    to_email: str,
    first_name: str,
    otp: str,
):
    text_body = f"""Hi {first_name},

Welcome to SignalOps!

To complete your registration, please use the verification code below to verify your email address.

Your verification code is: {otp}

Enter this code on the registration page to verify your email and activate your account.

For your security, this code will expire in {settings.otp_expire_minutes} minutes. Do not share this code with anyone.

If you did not attempt to register with SignalOps, you can safely ignore this email.

Best regards,
The SignalOps Team
"""

    html_template = templates.env.get_template("email/registration_otp.html")
    html_body = html_template.render(
        first_name=first_name,
        otp=otp,
        minutes=settings.otp_expire_minutes,
    )

    ses_client = get_boto3_ses_client()
    ses_client.send_email(
        Source=settings.mail_from,
        Destination={
            "ToAddresses": [to_email],
        },
        Message={
            "Subject": {
                "Data": "Verify Your Email - SignalOps",
                "Charset": "UTF-8",
            },
            "Body": {
                "Text": {
                    "Data": text_body,
                    "Charset": "UTF-8",
                },
                "Html": {
                    "Data": html_body,
                    "Charset": "UTF-8",
                },
            },
        },
    )
