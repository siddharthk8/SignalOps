from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.email_suppression import EmailSuppression, EmailSuppressionReason


class EmailSuppressionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(
        self,
        email: EmailStr,
        reason: EmailSuppressionReason,
    ) -> None:
        self.db.add(
            EmailSuppression(
                email=str(email).strip().lower(),
                reason=reason,
            )
        )

    async def get_with_email(self, email: EmailStr) -> EmailSuppression | None:
        result = await self.db.execute(
            select(EmailSuppression).where(
                EmailSuppression.email == str(email).strip().lower()
            )
        )
        return result.scalar_one_or_none()
