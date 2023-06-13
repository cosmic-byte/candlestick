import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from pydantic import condecimal


@dataclass
class Instrument:
    id: uuid.UUID
    isin: str
    created_at: datetime
    deleted_at: Optional[datetime] = None
    deleted: bool = False


@dataclass
class InstrumentPrice:
    id: uuid.UUID
    price: condecimal(max_digits=5, decimal_places=3)
    created_at: datetime


@dataclass
class Quote:
    """
    Value object representing a price update for an instrument
    """
    isin: str
    value: condecimal(max_digits=5, decimal_places=3)
    created_at: datetime


@dataclass
class CandleStick:
    open_price: condecimal(max_digits=5, decimal_places=3)
    high_price: condecimal(max_digits=5, decimal_places=3)
    low_price: condecimal(max_digits=5, decimal_places=3)
    close_price: condecimal(max_digits=5, decimal_places=3)
    open_timestamp: datetime
    close_timestamp: datetime
