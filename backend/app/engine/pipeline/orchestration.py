from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.batch import Batch
from app.db.models.source_app import SourceApp
from app.engine.pipeline.stages.ai import AIStage
from app.engine.pipeline.stages.correlation import CorrelationStage
from app.engine.pipeline.stages.parsing import ParsingStage
from app.engine.pipeline.stages.rule import RuleStage
from app.enums.common import SourceAppType
from app.schemas.analysis import IncidentAnalysis
from app.schemas.log import LogsField


class LogPipeline:
    def __init__(self, db: AsyncSession, batch_orm: Batch, source_app_orm: SourceApp):
        self.db = db
        self.batch_orm = batch_orm
        self.source_app_orm = source_app_orm

        self.parsing_stage = ParsingStage(db, batch_orm)
        self.ai_stage = AIStage(db, batch_orm)
        self.rule_stage = RuleStage(db)
        self.correlation_stage = CorrelationStage(db)

    async def process(self, logs: LogsField) -> list[IncidentAnalysis]:
        source_app = SourceAppType(self.source_app_orm.app_type)

        # parsing
        events, unresolved_logs = await self.parsing_stage.run(logs, source_app)

        if len(unresolved_logs) > 0:
            ai_events = await self.ai_stage.fallback_run(unresolved_logs, source_app)
            await self.parsing_stage.merge_ai_events(events, ai_events, unresolved_logs)

        # rule
        signals = await self.rule_stage.run(source_app=source_app, events=events)

        # correlation
        incidents = await self.correlation_stage.run(
            signals=signals, source_app=source_app
        )

        # ai analysis of incidents
        analyzed_incidents = await self.ai_stage.run(
            incidents=incidents, source_app=source_app
        )

        await self.db.commit()
        return analyzed_incidents
