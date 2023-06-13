import logging
from dataclasses import dataclass

from candlestick.domain.models.instrument import Quote

from candlestick.application.ports import Stream

from candlestick.application.unit_of_work import UnitOfWorkProvider
from candlestick.domain.utils import utc_now

_LOG = logging.getLogger(__name__)


@dataclass
class SubscribeQuoteStream:
    uow_provider: UnitOfWorkProvider
    quote_stream: Stream

    def __call__(self):
        self.quote_stream.connect(self._handle_message)

    def _handle_message(self, event: dict):
        """Handle quote message from stream, with format:
            {
                "data": { "price": 900.2013, "isin": "BP0725X33602" },
                "type": "QUOTE"
            }
        """
        quote_data = event["data"]
        _LOG.debug("creating new instrument price: %s", quote_data)
        quote = Quote(
            isin=quote_data["isin"],
            value=quote_data["price"],
            created_at=utc_now(),
        )
        with self.uow_provider.uow() as uow:
            uow.instrument_repo.add_price(quote)
            uow.commit()
