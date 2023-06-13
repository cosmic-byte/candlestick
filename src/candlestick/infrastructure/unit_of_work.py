from sqlalchemy import engine
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from candlestick.application.unit_of_work import UnitOfWork, UnitOfWorkProvider
from candlestick.domain.exceptions import PersistenceError
from candlestick.infrastructure.repositories.instrument import (
    MemoryInstrumentRepository,
    SQLInstrumentRepository,
)


class MemoryUnitOfWorkProvider(UnitOfWorkProvider):
    def __init__(self):
        self.memory_uow = MemoryUnitOfWork()

    def uow(self):
        return self.memory_uow


class MemoryUnitOfWork(UnitOfWork):
    def __init__(self):
        self.instrument_repo = MemoryInstrumentRepository()
        self.committed = False

    def __exit__(self, *args):
        pass

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


class SqlAlchemyUnitOfWorkProvider(UnitOfWorkProvider):
    def __init__(self, engine: engine.Engine, session_autoflush_on: bool = True):
        self.engine = engine
        self.session_auto_flush_on = session_autoflush_on

    def uow(self):
        return SqlAlchemyUnitOfWork(self.engine)


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, db_engine: engine.Engine, session_autoflush_on: bool = True):
        self.db_engine = db_engine
        self.session_autoflush_on = session_autoflush_on
        self.session = None

    def __enter__(self):
        self.session = Session(self.db_engine, autoflush=self.session_autoflush_on)
        self.instrument_repo = SQLInstrumentRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        self.session.close()

    def commit(self):
        try:
            self.session.commit()
        except IntegrityError as e:
            self.rollback()
            raise PersistenceError(str(e)) from e
        except Exception as e:
            self.rollback()
            raise e

    def rollback(self):
        self.session.rollback()
