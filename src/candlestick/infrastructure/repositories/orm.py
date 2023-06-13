import decimal
import uuid
from datetime import datetime
from typing import Optional

import sqlalchemy
from sqlmodel import Field, Relationship, SQLModel, create_engine

from candlestick.config import CONFIG


class Instrument(SQLModel, table=True):
    id: uuid.UUID = Field(nullable=False, primary_key=True, default_factory=uuid.uuid4, index=True)
    isin: str = Field(max_length=30, nullable=True)
    deleted: bool = Field(default=False)
    created_at: datetime = Field(
        sa_column=sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), nullable=False)
    )
    deleted_at: Optional[datetime] = Field(
        sa_column=sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), nullable=True)
    )


class InstrumentPrice(SQLModel, table=True):
    id: uuid.UUID = Field(nullable=False, primary_key=True, default_factory=uuid.uuid4, index=True)
    price: decimal.Decimal = Field(nullable=False)
    created_at: datetime = Field(
        sa_column=sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), nullable=False)
    )
    instrument_id: uuid.UUID = Field(foreign_key="instrument.id")
    instrument: Instrument = Relationship()


def init_db_engine(db_url: str) -> sqlalchemy.engine.Engine:
    """
    Connect to a bare SQL url, in case the DB does not exist, in which
    case create the DB, and then connect to it.
    """
    db_engine = create_engine(db_url)
    if CONFIG["app"]["env"] == "dev":
        SQLModel.metadata.create_all(db_engine)

    return db_engine
