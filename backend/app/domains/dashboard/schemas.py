from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
)

from app.domains.batch.schemas import IncidentResponse


class DashboardOverviewSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    source_apps_count: int
    incidents_count: int
    unresolved_incidents_count: int
    last_5_incidents: list[IncidentResponse]
    daily_incidents_over_last_30_days: list[dict[str, int | datetime]]
