import decimal
import uuid

import pytest
from candlestick.domain.models.instrument import Instrument, Quote

from candlestick.infrastructure.repositories.instrument import (
    MemoryInstrumentRepository,
    SQLInstrumentRepository,
)

from candlestick.infrastructure.unit_of_work import (
    SqlAlchemyUnitOfWorkProvider,
    MemoryUnitOfWorkProvider,
)
from sqlalchemy_utils import create_database, database_exists  # type: ignore
from sqlmodel import Session, SQLModel, create_engine

from candlestick.config import env


db_connection_string = env(
    "REPOSITORY_POSTGRES_TEST_DB_URL",
    "postgresql+psycopg2://postgres:password@127.0.0.1/test_candlestick",
)

@pytest.fixture
def postgres_engine():
    engine = create_engine(db_connection_string)

    if not database_exists(engine.url):
        create_database(engine.url)

    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def sql_uow_provider(postgres_engine):
    return SqlAlchemyUnitOfWorkProvider(postgres_engine, session_autoflush_on=False)


@pytest.fixture
def memory_uow_provider():
    return MemoryUnitOfWorkProvider()


@pytest.fixture
def memory_instrument_repository() -> MemoryInstrumentRepository:
    return MemoryInstrumentRepository()


@pytest.fixture
def sql_instrument_repository(postgres_engine) -> SQLInstrumentRepository:
    session = Session(postgres_engine, autoflush=True)
    return SQLInstrumentRepository(session)


@pytest.fixture
def create_instrument():
    def _create_instrument(id: uuid.UUID, isin: str, **kwargs) -> Instrument:
        return Instrument(id=id, isin=isin, **kwargs)
    return _create_instrument


@pytest.fixture
def create_quote():
    def _create_quote(isin: str, value: decimal, **kwargs) -> Quote:
        return Quote(isin=isin, value=value, **kwargs)
    return _create_quote
