from sqlalchemy.orm import Session

from app.db.repositories.refresh_token import RefreshTokenRepository
from app.db.repositories.user import UserRepository
from app.domains.users.dependencies import CurrentUser


async def revoke_all_refresh_tokens(current_user: CurrentUser, db: Session):
    user_repo = UserRepository(db)
    # to invalidate previous tokens
    user_repo.increment_token_version(current_user)

    rt_repo = RefreshTokenRepository(db)
    rt_repo.revoke_refresh_tokens(current_user)
    db.commit()
