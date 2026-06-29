from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import auth_logger
from app.db.repositories.refresh_token import RefreshTokenRepository
from app.domains.auth.schemas import (
    RefreshTokenRequest,
    RefreshTokenResponse,
)
from app.domains.auth.utils import (
    create_access_token,
    get_refresh_token_hash,
)


async def refresh_token(refresh_token_data: RefreshTokenRequest, db: AsyncSession):
    refresh_token = refresh_token_data.refresh_token
    token_hash = get_refresh_token_hash(refresh_token)

    rt_repo = RefreshTokenRepository(db)
    rt = await rt_repo.get_by_token_hash(token_hash)

    if rt is None:
        auth_logger.warning(
            "Authentication failed: refresh token not found. token=%s",
            refresh_token,
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Kindly re-login using your credentials.",
        )

    # DB returns naive datetime (in case of MySQL/sqlite3), so we attach tzinfo (since its already UTC)
    expires = rt.expires_at
    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=UTC)

    # compare using aware UTC time
    now = datetime.now(UTC)

    if rt.is_revoked or (expires < now):
        auth_logger.warning(
            "Authentication failed: refresh token rejected (invalid or expired). user_id=%s",
            rt.user_id,
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    user = rt.user
    access_token = create_access_token({"sub": str(user.id), "tv": user.token_version})

    await db.commit()
    return RefreshTokenResponse(access_token=access_token)
