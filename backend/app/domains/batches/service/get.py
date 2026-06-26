from fastapi import HTTPException, status

from app.db.core import DBSessionDep
from app.db.repositories.batch import BatchRepository
from app.db.repositories.event import EventRepository
from app.db.repositories.incident import IncidentRepository
from app.db.repositories.signal import SignalRepository
from app.domains.batches.schemas import (
    AIAnalysisResponse,
    EntityResponse,
    EventResponse,
    GetBatch,
    IncidentResponse,
    LogResponse,
    SignalResponse,
)
from app.domains.users.dependencies import CurrentUser


async def get_batch(batch_id: int, current_user: CurrentUser, db: DBSessionDep):
    batch_repo = BatchRepository(db)
    event_repo = EventRepository(db)
    signal_repo = SignalRepository(db)
    incident_repo = IncidentRepository(db)

    batch = await batch_repo.get(batch_id)

    if not batch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Batch does not exist.",
        )

    if batch.source_app.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authorized to perform this action.",
        )

    ai_analyses = batch.ai_analyses
    events = await event_repo.filter_for_response(batch_id)  # contains entity & log

    signals = []
    incidents = []

    unique_signal_ids = {e.signal_id for e in events if e.signal_id}
    if len(unique_signal_ids) > 0:
        signals = await signal_repo.filter_for_response(unique_signal_ids)
        unique_incident_ids = {s.incident_id for s in signals if s.incident_id}

        if len(unique_incident_ids) > 0:
            incidents = await incident_repo.filter_for_response(unique_signal_ids)

    all_entities = [EntityResponse.model_validate(e.entity) for e in events if e.entity]
    seen = set()
    entities = []

    for entity in all_entities:
        if entity.id not in seen:
            seen.add(entity.id)
            entities.append(entity)

    logs = [LogResponse.model_validate(e.log) for e in events]
    events = [EventResponse.model_validate(e) for e in events]
    signals = [SignalResponse.model_validate(s) for s in signals]
    incidents = [IncidentResponse.model_validate(i) for i in incidents]
    ai_analyses = [AIAnalysisResponse.model_validate(aia) for aia in ai_analyses]

    return GetBatch(
        id=batch.id,
        logs=logs,
        entities=entities,
        events=events,
        signals=signals,
        incidents=incidents,
        ai_analyses=ai_analyses,
        created_at=batch.created_at,
    )
