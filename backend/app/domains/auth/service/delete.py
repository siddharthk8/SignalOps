from sqlalchemy.orm import Session

from app.db.repositories.user import UserRepository
from app.domains.auth.dependencies import CurrentUser


async def delete_current_user(current_user: CurrentUser, db: Session):
    user_repo = UserRepository(db)
    user_repo.delete_user(current_user)
    db.commit()
