from decimal import Decimal
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from candlestick.domain.models.instrument import CandleStick


class CandleStickOut(BaseModel):
    open_timestamp: datetime
    close_timestamp: datetime
    open_price: Optional[Decimal] = None
    high_price: Optional[Decimal] = None
    low_price: Optional[Decimal] = None
    close_price: Optional[Decimal] = None

    @classmethod
    def from_domain(cls, candlestick: CandleStick):
        return cls(
            open_timestamp=candlestick.open_timestamp,
            close_timestamp=candlestick.close_timestamp,
            open_price=candlestick.open_price,
            close_price=candlestick.close_price,
            low_price=candlestick.low_price,
            high_price=candlestick.high_price,
        )
