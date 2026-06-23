from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db.repositories.refresh_token import RefreshTokenRepository
from app.domains.auth.schemas import (
    RefreshTokenRequest,
    RefreshTokenResponse,
)
from app.domains.auth.utils import (
    create_access_token,
    get_refresh_token_hash,
)


async def refresh_token(refresh_token_data: RefreshTokenRequest, db: Session):
    refresh_token = refresh_token_data.refresh_token
    token_hash = get_refresh_token_hash(refresh_token)

    rt_repo = RefreshTokenRepository(db)
    rt = rt_repo.get_by_token_hash(token_hash)

    if rt is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Kindly re-login using your credentials.",
        )

    # DB returns naive datetime (MySQL), so we attach tzinfo (since its already UTC)
    expires = rt.expires_at
    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=UTC)

    # compare using aware UTC time
    now = datetime.now(UTC)

    if rt.revoked or (expires < now):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    user = rt.user
    access_token = create_access_token({"sub": str(user.id), "tv": user.token_version})

    db.commit()
    return RefreshTokenResponse(access_token=access_token)
