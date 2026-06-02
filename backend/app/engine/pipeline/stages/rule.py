from sqlalchemy.orm import Session

from app.engine.rules.category.generic import GenericRule
from app.engine.rules.registery import RULE_REGISTRY
from app.schemas.signal import Signal


class RuleStage:
    def __init__(self, db: Session):
        self.db = db
        self.generic_rule = GenericRule()

    async def run(self, source_app, events):
        signals: list[Signal] = []

        # domain rules
        rule = RULE_REGISTRY.get(source_app)
        if rule:
            signals.extend(rule.evaluate(events))

        # generic rules
        signals.extend(self.generic_rule.evaluate(events))

        return signals
