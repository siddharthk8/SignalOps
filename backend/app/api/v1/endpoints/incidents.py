from fastapi import APIRouter, status

from app.db.core import DBSessionDep
from app.domains.incident import service
from app.domains.user.dependencies import CurrentUser

router = APIRouter()


@router.post(
    "/{incident_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def mark_incident_resolved(
    incident_id: int,
    current_user: CurrentUser,
    db: DBSessionDep,
):
    return await service.mark_incident_resolved(incident_id, current_user, db)
