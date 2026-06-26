from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.signal import SignalRepository
from app.engine.rules.category.generic import GenericRule
from app.engine.rules.registery import RULE_REGISTRY
from app.schemas.signal import Signal


class RuleStage:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.generic_rule = GenericRule()
        self.signal_repo = SignalRepository(db)

    async def run(self, source_app, events):
        signals: list[Signal] = []

        # domain rules
        rule = RULE_REGISTRY.get(source_app)
        if rule:
            signals.extend(rule.evaluate(events))

        # generic rules
        signals.extend(self.generic_rule.evaluate(events))

        # save signals in db
        await self.signal_repo.save_signals(signals=signals)

        return signals
