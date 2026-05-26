from app.engine.pipeline.stages.ai import AIStage
from app.engine.pipeline.stages.correlation import CorrelationStage
from app.engine.pipeline.stages.parsing import ParsingStage
from app.engine.pipeline.stages.rule import RuleStage
from app.schemas.analysis import IncidentAnalysis
from app.schemas.log import LogBatchRequest


class LogPipeline:
    def __init__(self):
        self.parsing_stage = ParsingStage()
        self.ai_stage = AIStage()
        self.rule_stage = RuleStage()
        self.correlation_stage = CorrelationStage()

    async def process(self, logs_batch: LogBatchRequest) -> list[IncidentAnalysis]:
        logs = logs_batch.logs
        source_app = logs_batch.source_app

        # parsing
        events, unresolved_logs = await self.parsing_stage.run(logs, source_app)

        if len(unresolved_logs) > 0:
            ai_events = await self.ai_stage.fallback_run(unresolved_logs, source_app)
            self.parsing_stage.merge_ai_events(events, ai_events, unresolved_logs)

        # rule
        signals = await self.rule_stage.run(source_app=source_app, events=events)

        # correlation
        incidents = await self.correlation_stage.run(signals=signals)

        # ai analysis of incidents
        analyzed_incidents = await self.ai_stage.run(incidents=incidents)

        return analyzed_incidents


log_pipeline = LogPipeline()
