import logging
from dataclasses import dataclass
from datetime import timedelta
from typing import List

from candlestick.domain.models.instrument import CandleStick

from candlestick.application.unit_of_work import UnitOfWorkProvider
from candlestick.domain.exceptions import InvalidInstrumentISINException
from candlestick.domain.utils import utc_now, round_down_to_min

_LOG = logging.getLogger(__name__)


@dataclass
class GetCandleSticks:
    uow_provider: UnitOfWorkProvider

    def __call__(self, isin: str, interval_in_min: int = 30) -> List[CandleStick]:
        """
        Provide a list of candlestick for the given interval in minutes (default 30min).

        :param isin: The unique identifier of each instrument.
        :param interval_in_min: The candlestick window
        :return: List of candlesticks
        """
        end_date = round_down_to_min(utc_now())
        start_date = end_date - timedelta(minutes=interval_in_min)

        _LOG.debug("retrieving candlesticks for instrument: %s", isin)
        with self.uow_provider.uow() as uow:
            try:
                candlesticks = uow.instrument_repo.get_candlesticks(
                    isin=isin, start_date=start_date, end_date=end_date
                )
            except KeyError:
                _err = f"No instrument with isin {isin} found"
                _LOG.debug(_err)
                raise InvalidInstrumentISINException(reason=_err)
        _LOG.info("retrieved %s candlesticks for isin %s", len(candlesticks), isin)
        return candlesticks
