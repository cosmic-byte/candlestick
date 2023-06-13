from typing import Callable, Union

from candlestick.application.ports import Stream


class MemoryInstrumentStream(Stream):
    def connect(self, handler: Callable[[Union[dict, list]], None]):
        pass

    def __init__(self):
        pass

    def on_message(self, connection, message):
        pass

    def on_error(self, connection, error):
        pass

    def on_close(self, connection, close_status_code, close_msg):
        pass

    def on_open(self, connection):
        pass


class MemoryQuoteStream(Stream):
    def connect(self, handler: Callable[[Union[dict, list]], None]):
        pass

    def on_message(self, connection, message):
        pass

    def on_error(self, connection, error):
        pass

    def on_close(self, connection, close_status_code, close_msg):
        pass

    def on_open(self, connection):
        pass
