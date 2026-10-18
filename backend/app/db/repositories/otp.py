from datetime import date

from pydantic import EmailStr
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.otp import Otp


class OtpRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, otp_hash: str, email: EmailStr, expires_at: date):
        self.db.add(Otp(otp_hash=otp_hash, count=1, email=email, expires_at=expires_at))

    async def get_otp_object_by_email(self, email: EmailStr):
        query = await self.db.execute(select(Otp).where(Otp.email == email))
        result = query.scalar_one_or_none()
        return result

    async def update_otp_hash(self, otp_hash: str, email: EmailStr, expires_at: date):
        await self.db.execute(
            update(Otp)
            .where(Otp.email == email)
            .values(otp_hash=otp_hash, expires_at=expires_at, count=Otp.count + 1)
        )
