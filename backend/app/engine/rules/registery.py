from collections.abc import Mapping

from app.engine.rules.base import BaseRule
from app.engine.rules.category.auth import AuthRule
from app.engine.rules.category.order import OrderRule
from app.engine.rules.category.payment import PaymentRule
from app.enums.common import SourceAppType

RULE_REGISTRY: Mapping[SourceAppType, BaseRule] = {
    SourceAppType.AUTH_APP: AuthRule(),
    SourceAppType.ORDER_APP: OrderRule(),
    SourceAppType.PAYMENT_APP: PaymentRule(),
}
