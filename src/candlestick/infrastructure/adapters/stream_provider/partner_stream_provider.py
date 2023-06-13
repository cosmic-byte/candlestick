import abc
import json
import logging
from typing import Callable, Union

import websocket

from candlestick.application.ports import Stream

_LOG = logging.getLogger(__name__)


class PartnerStream(Stream, abc.ABC):

    @abc.abstractmethod
    def __init__(self, host, port):
        pass

    def on_error(self, connection, error):
        pass

    def on_close(self, connection, close_status_code, close_msg):
        pass

    def on_open(self, connection):
        pass


class PartnerInstrumentStream(PartnerStream):

    def __init__(self, host, port):
        self.handler = None
        self.socket_url = f"{host}:{port}/instruments"
        self.socket = websocket.WebSocketApp(
            self.socket_url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )

    def connect(self, handler: Callable[[Union[dict, list]], None]):
        _LOG.info("connecting to instrument stream server, with url: %s", self.socket_url)
        self.handler = handler
        self.socket.run_forever()

    def on_message(self, connection, message):
        _LOG.debug("received instrument event: %s", message)
        self.handler(json.loads(message))


class PartnerQuoteStream(PartnerStream):

    def __init__(self, host, port):
        self.handler = None
        self.socket_url = f"{host}:{port}/quotes"
        self.socket = websocket.WebSocketApp(
            self.socket_url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )

    def connect(self, handler: Callable[[Union[dict, list]], None]):
        _LOG.info("connecting to quotes stream server, with url: %s", self.socket_url)
        self.handler = handler
        self.socket.run_forever()

    def on_message(self, connection, message):
        _LOG.debug("received quote: %s", message)
        self.handler(json.loads(message))
