from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.incident import IncidentRepository
from app.domains.user.dependencies import CurrentUser


async def mark_incident_resolved(
    incident_id: int, current_user: CurrentUser, db: AsyncSession
):
    incident_repo = IncidentRepository(db)
    incident_model = await incident_repo.get_by_id(incident_id)

    if incident_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incident does not exist."
        )

    if incident_model.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authorized to perform this action.",
        )

    await incident_repo.save_resolved_at(incident_model.id)
    await db.commit()
