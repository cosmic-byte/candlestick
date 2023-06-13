from typing import List

from fastapi import FastAPI, Depends, HTTPException
from starlette import status
from starlette.responses import RedirectResponse

from candlestick.dependency_container import Application, _LOG
from candlestick.domain.models.instrument import CandleStick

from .models import CandleStickOut
from ...domain.exceptions import InvalidInstrumentISINException

app = FastAPI(
    title="Candlestick API",
    description="Return candlestick for 30 min interval.",
    version="0.0.1",
    docs_url="/",
)


@app.get("/docs", name="Openapi UI", tags=["utils"])
async def docs_url():
    return RedirectResponse("/")


@app.get(
    "/healthcheck/",
    name="Health check",
    description="Check health of the service.",
    tags=["utils"],
)
async def healthcheck() -> dict:
    return {"msg": "OK"}


@app.get(
    "/candlesticks",
    response_model=List[CandleStickOut],
    response_description="Returns candlesticks for an instrument",
)
async def provide_candlesticks(isin: str, application: Application = Depends()):
    """
    Returns candlesticks for an instrument
    """
    use_case = application.get_candlesticks
    try:
        candlesticks: List[CandleStick] = use_case(isin=isin)
        return [CandleStickOut.from_domain(candlestick) for candlestick in candlesticks]
    except InvalidInstrumentISINException as err:
      _LOG.debug(str(err))
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from err
    except Exception as err:
        # Todo: properly handle possible exceptions
        _LOG.error(str(err))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from err


@app.on_event("startup")
async def startup_event():
    # As Application is a singleton we create the application here,
    # in order to not slow down the first user-request.
    Application()
