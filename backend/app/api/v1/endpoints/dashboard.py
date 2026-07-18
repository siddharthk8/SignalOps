from fastapi import APIRouter, Depends, status

from app.core.rate_limiter.dependencies import user_rate_limit
from app.db.core import DBSessionDep
from app.domains.dashboard import service
from app.domains.dashboard.schemas import DashboardOverviewSchema
from app.domains.user.dependencies import CurrentUser

router = APIRouter()


@router.get(
    "",
    response_model=DashboardOverviewSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(user_rate_limit(capacity=20, refill_rate=2))],
)
async def dashboard_overview(current_user: CurrentUser, db: DBSessionDep):
    return await service.dashboard_overview(current_user, db)
