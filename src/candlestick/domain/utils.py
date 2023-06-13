from __future__ import annotations

from datetime import datetime, timezone, timedelta
from decimal import Decimal
from enum import Enum
from typing import Optional
from uuid import UUID


def cast(value):
    if isinstance(value, (UUID, Decimal)):
        value = str(value)
    if isinstance(value, Enum):
        value = value.value
    if isinstance(value, datetime):
        value = value.isoformat()
    if isinstance(value, dict):
        value = {k: cast(v) for (k, v) in value.items()}
    return value


def parse_uuid(id_) -> UUID:
    if id_ and isinstance(id_, UUID):
        return id_

    return UUID(id_)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def round_down_to_min(date_time: Optional[datetime]) -> Optional[datetime]:
    """
    Round down a datetime to the current minute ie: clearing out the seconds and microseconds
    eg: 2019-03-05 13:03:56:004 --> 2019-03-05 13:03:00:000
    :param date_time:
    :return:
    """
    if not date_time:
        return None
    return date_time.replace(second=0, microsecond=0)


def round_up_to_min(date_time: Optional[datetime]) -> Optional[datetime]:
    """
    Round up a datetime to the next minute ie: clearing out the seconds and microseconds
    eg: 2019-03-05 13:03:56:004 --> 2019-03-05 13:04:00:000
    :param date_time:
    :return:
    """
    if not date_time:
        return None

    if date_time.microsecond == date_time.second == 0:
        return date_time
    date_time = date_time.replace(second=0, microsecond=0)
    return date_time + timedelta(minutes=1)
