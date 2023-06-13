import uuid
from datetime import timedelta

from candlestick.domain.utils import utc_now, round_down_to_min


def test_get_get_instrument_prices(sql_uow_provider, create_instrument, create_quote):
    inst_1 = create_instrument(id=uuid.uuid4(), isin="W3FS4FF1", created_at=utc_now())
    inst_2 = create_instrument(id=uuid.uuid4(), isin="W3FS4FF2", created_at=utc_now())

    with sql_uow_provider.uow() as uow:
        uow.instrument_repo.add(inst_1)
        uow.instrument_repo.add(inst_2)
        uow.commit()

    with sql_uow_provider.uow() as uow:
        for i in range(10):
            _created_at = utc_now() - timedelta(seconds=20*i)
            quote = create_quote(isin="W3FS4FF2", value=100 + i, created_at=_created_at)
            uow.instrument_repo.add_price(quote)
            quote = create_quote(isin="W3FS4FF2", value=10 + i, created_at=_created_at)
            uow.instrument_repo.add_price(quote)
            quote = create_quote(isin="W3FS4FF2", value=200 + i, created_at=_created_at)
            uow.instrument_repo.add_price(quote)

            _created_at = utc_now() - timedelta(minutes=i)
            quote = create_quote(isin="W3FS4FF1", value=100 - i, created_at=_created_at)
            uow.instrument_repo.add_price(quote)
        uow.commit()

    end_date = round_down_to_min(utc_now())
    start_date = end_date - timedelta(minutes=30)

    with sql_uow_provider.uow() as uow:
       candlesticks = uow.instrument_repo.get_candlesticks(
           isin="W3FS4FF2",
           start_date=start_date,
           end_date=end_date,
       )

    assert len(candlesticks) == 30
