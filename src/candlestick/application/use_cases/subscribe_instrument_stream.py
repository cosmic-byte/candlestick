import logging
import uuid
from dataclasses import dataclass
from enum import Enum

from candlestick.domain.models.instrument import Instrument

from candlestick.application.ports import Stream

from candlestick.application.unit_of_work import UnitOfWorkProvider
from candlestick.domain.utils import utc_now

_LOG = logging.getLogger(__name__)


class EventType(Enum):
    ADD = "add"
    DELETE = "delete"


@dataclass
class SubscribeInstrumentStream:
    uow_provider: UnitOfWorkProvider
    instrument_stream: Stream

    def __call__(self):
        self.instrument_stream.connect(self._handle_message)

    def _handle_message(self, event: dict):
        """Handle message from stream, with format:
            {
                "data": {
                    "description": "impetus sagittis graeco quot", "isin": "MU5137356340"
                },
                "type": "ADD"
            }
        """
        instrument_data = event["data"]
        if event["type"].lower() == EventType.ADD.value:
            _LOG.debug("creating new instrument: %s", event)
            instrument = Instrument(
                id=uuid.uuid4(),
                isin=instrument_data["isin"],
                created_at=utc_now(),
            )
            with self.uow_provider.uow() as uow:
                uow.instrument_repo.add(instrument)
                uow.commit()
        else:
            isin = instrument_data["isin"]
            _LOG.debug("deleting instrument by isin: %s", isin)

            with self.uow_provider.uow() as uow:
                uow.instrument_repo.delete_by_isin(isin)
                uow.commit()
