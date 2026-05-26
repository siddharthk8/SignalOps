from app.engine.pipeline.stages.ai_stage import AIStage
from app.engine.pipeline.stages.parsing_stage import ParsingStage
from app.engine.pipeline.stages.rule_stage import RuleStage
from app.schemas.log import LogBatchRequest, LogBatchResponse


class LogPipeline:
    def __init__(self):
        self.parsing_stage = ParsingStage()
        self.ai_stage = AIStage()
        self.rule_stage = RuleStage()

    async def process(self, logs_batch: LogBatchRequest) -> LogBatchResponse:
        logs = logs_batch.logs
        source_app = logs_batch.source_app

        # parsing
        events, unresolved_logs = await self.parsing_stage.run(logs, source_app)

        if len(unresolved_logs) > 0:
            ai_events = await self.ai_stage.fallback_run(unresolved_logs, source_app)
            self.parsing_stage.merge_ai_events(events, ai_events, unresolved_logs)

        # rule
        signals = await self.rule_stage.run(source_app=source_app, events=events)

        # ...
        return LogBatchResponse()


log_pipeline = LogPipeline()
