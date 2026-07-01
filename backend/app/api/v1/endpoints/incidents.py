from fastapi import APIRouter, Depends, status

from app.core.rate_limiter.dependencies import user_rate_limit
from app.db.core import DBSessionDep
from app.domains.incident import service
from app.domains.user.dependencies import CurrentUser

router = APIRouter()


@router.post(
    "/{incident_id}/resolve",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(user_rate_limit(capacity=10, refill_rate=0.2))],
)
async def mark_incident_resolved(
    incident_id: int,
    current_user: CurrentUser,
    db: DBSessionDep,
):
    return await service.mark_incident_resolved(incident_id, current_user, db)
