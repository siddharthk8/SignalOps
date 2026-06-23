from datetime import UTC, datetime

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.db.models.refresh_token import RefreshToken as ORMRefreshToken
from app.db.models.user import User
from app.domains.auth.schemas import RefreshToken


class RefreshTokenRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_refresh_token(self, refresh_token_obj: RefreshToken):
        self.db.add(ORMRefreshToken(**refresh_token_obj.model_dump()))
        self.db.flush()

    def revoke_refresh_tokens(self, user: User):
        self.db.execute(
            update(ORMRefreshToken)
            .where(
                ORMRefreshToken.user_id == user.id, ORMRefreshToken.revoked_at.is_(None)
            )
            .values(revoked=True, revoked_at=datetime.now(UTC))
        )

    def get_by_token_hash(self, token_hash: str) -> ORMRefreshToken | None:
        return self.db.execute(
            select(ORMRefreshToken).where(
                ORMRefreshToken.token_hash == token_hash,
            )
        ).scalar_one_or_none()
