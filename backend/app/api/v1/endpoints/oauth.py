from fastapi import APIRouter, Depends, status

from app.core.rate_limiter.dependencies import public_rate_limit
from app.db.core import DBSessionDep
from app.domains.oauth import service
from app.domains.oauth.schemas import GetOAuthConnections, GoogleLoginRequest
from app.domains.user.dependencies import CurrentUser

router = APIRouter()


@router.post(
    "/google",
    dependencies=[Depends(public_rate_limit(capacity=20, refill_rate=0.1))],
)
async def google_login(
    data: GoogleLoginRequest,
    db: DBSessionDep,
):
    return await service.google_login(data, db)


@router.get(
    "/oauth-connections",
    response_model=GetOAuthConnections,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(public_rate_limit(capacity=60, refill_rate=1))],
)
async def get_oauth_connections(current_user: CurrentUser, db: DBSessionDep):
    return await service.get_oauth_connections(current_user, db)


@router.post(
    "/link-google",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(public_rate_limit(capacity=80, refill_rate=2))],
)
async def link_google_account(
    data: GoogleLoginRequest,
    current_user: CurrentUser,
    db: DBSessionDep,
):
    return await service.link_google_account(data, current_user, db)
