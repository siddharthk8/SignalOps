from app.engine.pipeline.stages.ai_stage import AIStage
from app.engine.pipeline.stages.parsing_stage import ParsingStage
from app.schemas.log import LogBatchRequest, LogBatchResponse


class LogPipeline:
    def __init__(self):
        self.parsing_stage = ParsingStage()
        self.ai_stage = AIStage()

    async def process(self, logs_batch: LogBatchRequest) -> LogBatchResponse:
        logs = logs_batch.logs
        source_app = logs_batch.source_app

        # parsing
        events, unresolved_logs = await self.parsing_stage.run(logs, source_app)

        if len(unresolved_logs) > 0:
            ai_events = await self.ai_stage.fallback_run(unresolved_logs, source_app)
            self.parsing_stage.merge_ai_events(events, ai_events, unresolved_logs)

        print(len(events))
        for e in events:
            print(e.model_dump_json(indent=2))

        # ...
        return LogBatchResponse()


log_pipeline = LogPipeline()
