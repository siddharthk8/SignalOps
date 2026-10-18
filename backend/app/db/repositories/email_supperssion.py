from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.email_suppression import EmailSuppression, EmailSuppressionReason


class EmailSupperession:
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
