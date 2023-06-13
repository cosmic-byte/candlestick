import logging
from typing import List

import pinject
from singleton_decorator import singleton  # type: ignore

from candlestick.application import ports, use_cases
from candlestick.config import CONFIG
from candlestick.infrastructure import adapters, unit_of_work
from candlestick.infrastructure.repositories import orm

_LOG = logging.getLogger(__name__)


def setup_logger():
    logger_type = CONFIG["app"]["logger"]
    if logger_type == "console":
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s | %(message)s")
        handler.setFormatter(formatter)
        level = logging.INFO
    else:
        raise ValueError(f"Unknown logger type: {logger_type}")

    logging.root.addHandler(handler)
    logging.root.setLevel(logging.DEBUG)

    logger = logging.getLogger("candlestick")
    logger.setLevel(level)


class RepositoryBindings(pinject.BindingSpec):
    """
    Bind appropriate repository engine (memory, db, etc.) according to config
    """
    def configure(self, bind):
        repository_type = CONFIG["repository"]["type"]
        if repository_type == "postgres":
            db_engine = orm.init_db_engine(CONFIG["repository"]["postgres"]["db_url"])
            bind(
                "uow_provider",
                to_instance=unit_of_work.SqlAlchemyUnitOfWorkProvider(engine=db_engine),
            )
        else:
            raise ValueError(f"Unknown repository type {repository_type}")


class AdapterBindings(pinject.BindingSpec):
    def configure(self, bind):
        self.configure_stream_provider(bind)

    @staticmethod
    def configure_stream_provider(bind) -> None:
        conf = CONFIG["port"]["stream_provider"]
        instrument_stream: ports.stream_provider.Stream
        quote_stream: ports.stream_provider.Stream

        if conf["type"] == "partner":
            instrument_stream = adapters.stream_provider.PartnerInstrumentStream(
                host=conf["partner"]["host"], port=conf["partner"]["port"]
            )
            quote_stream = adapters.stream_provider.PartnerQuoteStream(
                host=conf["partner"]["host"], port=conf["partner"]["port"]
            )
        else:
            instrument_stream = adapters.stream_provider.MemoryInstrumentStream()
            quote_stream = adapters.stream_provider.MemoryQuoteStream()

        bind("instrument_stream", to_instance=instrument_stream)
        bind("quote_stream", to_instance=quote_stream)


@singleton
class Application:
    def __init__(self, bindings=None) -> None:
        """
        Use cases should be provided here

        e.g.: `object_graph.provide(use_case)`
        """
        setup_logger()

        object_graph = self._get_object_graph(bindings)

        self.get_candlesticks: use_cases.GetCandleSticks = object_graph.provide(
            use_cases.GetCandleSticks
        )
        self.subscribe_instrument_stream: use_cases.SubscribeInstrumentStream = object_graph.provide(
            use_cases.SubscribeInstrumentStream
        )
        self.subscribe_quote_stream: use_cases.SubscribeQuoteStream = object_graph.provide(
            use_cases.SubscribeQuoteStream
        )

    def __call__(self):
        return self

    @staticmethod
    def _get_object_graph(
        bindings: List[pinject.BindingSpec] = None,
    ) -> pinject.object_graph.ObjectGraph:
        if bindings is None:
            bindings = [RepositoryBindings(), AdapterBindings()]

        return pinject.new_object_graph(
            modules=None,
            classes=[
                # use cases go here
                use_cases.GetCandleSticks,
                use_cases.SubscribeInstrumentStream,
                use_cases.SubscribeQuoteStream,
            ],
            binding_specs=bindings,
        )
