import click

from candlestick.dependency_container import Application

from .subscribe_instrument_stream import subscribe_instrument_stream
from .subscribe_quote_stream import subscribe_quote_stream

app = Application()


@click.group()
@click.pass_context
def main(context):
    context.obj = app


main.add_command(subscribe_instrument_stream)
main.add_command(subscribe_quote_stream)
