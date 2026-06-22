import uuid

from sqlalchemy.orm import Session

from app.db.models.user import User
from app.db.repositories.user import UserRepository
from app.domains.auth.utils import DUMMY_HASH, verify_password


def get_user(db: Session, id: uuid.UUID) -> User | None:
    user = UserRepository(db).get_by_id(id)
    return user


def authenticate_user(db: Session, id: uuid.UUID, password: str) -> bool:
    user = get_user(db, id)
    if user is None:
        # Using a dummy hash to ensure authentication takes roughly the same time
        # whether or not the user exists, minimizing timing-based information leakage.
        verify_password(password, DUMMY_HASH)
        return False

    if not verify_password(password, user.password_hash):
        return False

    return True
