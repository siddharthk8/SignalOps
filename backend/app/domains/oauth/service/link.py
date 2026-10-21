from functools import partial

from fastapi import HTTPException, status
from fastapi.concurrency import run_in_threadpool
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.repositories.oauth_account import OAuthAccountRepository
from app.domains.oauth.schemas import GoogleLoginRequest
from app.domains.user.dependencies import CurrentUser


async def link_google_account(
    data: GoogleLoginRequest,
    current_user: CurrentUser,
    db: AsyncSession,
):
    try:
        google_user = await run_in_threadpool(
            partial(
                id_token.verify_oauth2_token,
                data.credential,
                google_requests.Request(),
                settings.google_client_id,
            )
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired Google credential",
        ) from exc

    google_sub = google_user.get("sub")
    email = google_user.get("email")
    email_verified = google_user.get("email_verified") is True

    if not google_sub or not email or not email_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="A verified Google email is required",
        )

    oauth_repo = OAuthAccountRepository(db)

    await oauth_repo.save_for_google(
        user_id=current_user.id,
        sub_id=google_sub,
    )
    await db.commit()
