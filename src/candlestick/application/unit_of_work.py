from __future__ import annotations

import abc

from candlestick.application import repositories


class UnitOfWorkProvider(abc.ABC):
    def uow(self) -> UnitOfWork:
        pass


class UnitOfWork(abc.ABC):
    instrument_repo: repositories.InstrumentRepository

    def __enter__(self) -> UnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError
