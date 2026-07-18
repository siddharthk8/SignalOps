from app.db.core import DBSessionDep
from app.db.repositories.incident import IncidentRepository
from app.db.repositories.source_app import SourceAppRepository
from app.domains.user.dependencies import CurrentUser


async def dashboard_overview(current_user: CurrentUser, db: DBSessionDep):
    source_app_repo = SourceAppRepository(db)
    incident_repo = IncidentRepository(db)

    source_apps_count = await source_app_repo.get_count_by_user(current_user.id)
    incidents_count = await incident_repo.get_count_by_user(current_user.id)

    unresolved_incidents_count = (
        await incident_repo.get_count_unresolved_events_by_user(current_user.id)
    )
    daily_incidents_over_last_30_days = (
        await incident_repo.get_daily_incidents_over_last_30_days_by_user(
            current_user.id
        )
    )
    last_5_incidents = await incident_repo.get_last_5_incidents_by_user(current_user.id)

    return {
        "source_apps_count": source_apps_count,
        "incidents_count": incidents_count,
        "unresolved_incidents_count": unresolved_incidents_count,
        "last_5_incidents": last_5_incidents,
        "daily_incidents_over_last_30_days": [
            {"date": row.date, "count": row.count}
            for row in daily_incidents_over_last_30_days
        ],
    }
