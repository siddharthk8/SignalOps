from fastapi import HTTPException, status

from app.db.core import DBSessionDep
from app.db.repositories.batch import BatchRepository
from app.db.repositories.event import EventRepository
from app.db.repositories.event_signal import EventSignalRepository
from app.db.repositories.incident import IncidentRepository
from app.db.repositories.signal import SignalRepository
from app.db.repositories.signal_incident import SignalIncidentRepository
from app.domains.batch.schemas import (
    AIAnalysisResponse,
    EntityResponse,
    EventResponse,
    GetBatch,
    IncidentResponse,
    LogResponse,
    SignalResponse,
)
from app.domains.user.dependencies import CurrentUser


async def get_batch(batch_id: int, current_user: CurrentUser, db: DBSessionDep):
    batch_repo = BatchRepository(db)
    event_repo = EventRepository(db)
    event_signal_repo = EventSignalRepository(db)
    signal_incident_repo = SignalIncidentRepository(db)

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

    event_ids = {e.id for e in events}
    if len(event_ids) > 0:
        event_signals = await event_signal_repo.filter_for_response(event_ids)
        u_signal_ids = {o.signal_id for o in event_signals}
        signals = await SignalRepository(db).filter_for_response(u_signal_ids)

        if len(signals) > 0:
            signal_incidents = await signal_incident_repo.filter_for_response(
                u_signal_ids
            )
            u_incident_ids = {o.incident_id for o in signal_incidents}
            incidents = await IncidentRepository(db).filter_for_response(u_incident_ids)

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
