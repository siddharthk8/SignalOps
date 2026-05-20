from collections.abc import Mapping

from app.enums.common import SourceAppType

from .base import BaseParser
from .parsers.auth.parser import AuthParser
from .parsers.order.parser import OrderParser
from .parsers.payment.parser import PaymentParser

PARSER_REGISTRY: Mapping[SourceAppType, BaseParser] = {
    SourceAppType.AUTH_APP: AuthParser(),
    SourceAppType.ORDER_APP: OrderParser(),
    SourceAppType.PAYMENT_APP: PaymentParser(),
}
