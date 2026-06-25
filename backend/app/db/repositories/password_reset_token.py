from datetime import datetime
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.orm import Session, selectinload

from app.db.models.password_reset_token import PasswordResetToken


class PasswordResetTokenRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_token_hash(self, token_hash: str) -> PasswordResetToken | None:
        return self.db.execute(
            select(PasswordResetToken)
            .options(selectinload(PasswordResetToken.user))
            .where(PasswordResetToken.token_hash == token_hash)
        ).scalar_one_or_none()

    def create(self, token_hash: str, user_id: UUID, expires_at: datetime):
        self.db.add(
            PasswordResetToken(
                token_hash=token_hash, user_id=user_id, expires_at=expires_at
            )
        )
        self.db.flush()

    def delete_all(self, user_id: UUID):
        self.db.execute(
            delete(PasswordResetToken).where(PasswordResetToken.user_id == user_id)
        )
