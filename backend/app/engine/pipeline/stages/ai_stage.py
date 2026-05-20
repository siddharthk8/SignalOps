from app.engine.parsing.parsers.ai_fallback import ai_fallback_parser
from app.enums.common import SourceAppType
from app.schemas.event import SemanticEvent
from app.schemas.log import LogField


class AIStage:
    async def fallback_run(
        self, unresolved_logs: list[tuple[int, LogField]], source_app: SourceAppType
    ) -> list[SemanticEvent]:
        ai_events = await ai_fallback_parser.parse(unresolved_logs, source_app)
        return ai_events
