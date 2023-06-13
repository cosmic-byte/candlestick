import abc
from typing import Callable, Union


class Stream(abc.ABC):
    @abc.abstractmethod
    def connect(self, handler: Callable[[Union[dict, list]], None]):
        pass

    @abc.abstractmethod
    def on_message(self, connection, message):
        pass

    @abc.abstractmethod
    def on_error(self, connection, error):
        pass

    @abc.abstractmethod
    def on_close(self, connection, close_status_code, close_msg):
        pass

    @abc.abstractmethod
    def on_open(self, connection):
        pass
