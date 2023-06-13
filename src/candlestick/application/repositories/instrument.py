import abc
from datetime import datetime
from typing import List

from candlestick.domain.models.instrument import Instrument, Quote, CandleStick


class InstrumentRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, instrument: Instrument) -> None:
        pass

    @abc.abstractmethod
    def delete_by_isin(self, isin: str) -> None:
        pass

    @abc.abstractmethod
    def add_price(self, quote: Quote) -> None:
        pass

    @abc.abstractmethod
    def get_candlesticks(
        self, isin: str, start_date: datetime, end_date: datetime
    ) -> List[CandleStick]:
        pass
