from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import exc
from sqlmodel import Session, select, text

from candlestick.application.repositories import InstrumentRepository
from candlestick.domain.models.instrument import Instrument, InstrumentPrice, Quote, CandleStick
from candlestick.domain.utils import utc_now, round_down_to_min, round_up_to_min
from candlestick.infrastructure.repositories import orm


class MemoryInstrumentRepository(InstrumentRepository):

    def __init__(self):
        self.instruments = {}
        self.instrument_prices = {}

    def delete_by_isin(self, isin: str) -> None:
        pass

    def add_price(self, quote: Quote) -> None:
        pass

    def get_candlesticks(
        self, isin: str, start_date: datetime, end_date: datetime
    ) -> List[CandleStick]:
        pass

    def add(self, instrument: Instrument) -> None:
        pass


class SQLInstrumentRepository(InstrumentRepository):
    def __init__(self, session: Session):
        self.session = session

    def delete_by_isin(self, isin: str) -> None:
        """
        Delete an instrument by it's isin.
        Note that this is a soft deletion.
        :param isin: unique identifier of an instrument
        :return: None
        """
        orm_instrument = self._get_orm_instrument_by_isin(isin)
        orm_instrument.deleted = True
        orm_instrument.deleted_at = utc_now()
        self.session.add(orm_instrument)

    def add_price(self, quote: Quote) -> None:
        """
        Create a new price instance of an instrument.
        :param quote: contains an updated price value of an instrument
        :return: None
        """
        orm_instrument = self._get_orm_instrument_by_isin(quote.isin)
        instrument_price = orm.InstrumentPrice(
            instrument=orm_instrument,
            price=quote.value,
            created_at=quote.created_at,
        )
        self.session.add(instrument_price)

    def get_candlesticks(
        self, isin: str, start_date: datetime, end_date: datetime
    ) -> Optional[List[CandleStick]]:
        """
        Returns the prices for an instrument within a specified start_date and end_date.
        Includes the lower bound (start_date) and excludes the upper bound (end_date)
        """
        orm_instrument = self._get_orm_instrument_by_isin(isin)

        statement = text(
            """
                with minutes as (
                  select generate_series(
                    :st,
                    :en - '1 minute'::interval,
                    '1 minute'::interval
                  ) as minute
                )
            
                select
                  minutes.minute as time_interval,
                  min(instrumentprice.price) as low_price,
                  max(instrumentprice.price) as high_price,
                  (ARRAY_AGG(price ORDER BY created_at ASC)  FILTER (where date_trunc('minute', 
                  created_at) = minutes.minute))[1] as open_price,
                  (ARRAY_AGG(price ORDER BY created_at DESC)  FILTER (where date_trunc('minute', 
                  created_at) = minutes.minute))[1] as close_price,
                  (ARRAY_AGG(created_at ORDER BY created_at ASC)  FILTER (where date_trunc('minute', 
                  created_at) = minutes.minute))[1] as open_timestamp,
                  (ARRAY_AGG(created_at ORDER BY created_at DESC)  FILTER (where date_trunc('minute', 
                  created_at) = minutes.minute))[1] as close_timestamp
                  
                from minutes
                left join instrumentprice on date_trunc('minute', instrumentprice.created_at) = minutes.minute
                and instrument_id = :inst
                group by time_interval
                order by time_interval;
            """
        )
        statement = statement.bindparams(
            st=start_date,
            en=end_date,
            inst=orm_instrument.id,
        )
        result = self.session.execute(statement)
        return [
            CandleStick(
                low_price=item[1],
                high_price=item[2],
                open_price=item[3],
                close_price=item[4],
                open_timestamp=round_down_to_min(item[5]),
                close_timestamp=round_up_to_min(item[6]),
            )
            for item in result.all()
        ]

    def add(self, instrument: Instrument) -> None:
        """
        Create an instance of an instrument
        :param instrument: dataclass containing instrument details
        :return: None
        """
        orm_instrument = _marshal_instrument(instrument)
        self.session.add(orm_instrument)

    def _get_orm_instrument_by_isin(self, isin: str) -> orm.Instrument:
        """
        Get orm instrument.
        :param isin: unique identifier of an instrument
        :return: orm instrument instance.
        """
        statement = select(orm.Instrument).where(
            orm.Instrument.isin == isin,
            orm.Instrument.deleted == False,   # type: ignore
        )
        result = self.session.exec(statement)
        try:
            instrument = result.one()
        except exc.NoResultFound as e:
            raise KeyError from e
        return instrument


def _marshal_instrument(instrument: Instrument) -> orm.Instrument:
    return orm.Instrument(
        id=instrument.id,
        isin=instrument.isin,
        created_at=instrument.created_at,
        deleted=instrument.deleted,
        deleted_at=instrument.deleted,
    )


def _unmarshal_instrument_price(orm_instrument_price: orm.InstrumentPrice) -> InstrumentPrice:
    return InstrumentPrice(
        id=orm_instrument_price.id,
        price=orm_instrument_price.price,
        created_at=orm_instrument_price.created_at,
    )
