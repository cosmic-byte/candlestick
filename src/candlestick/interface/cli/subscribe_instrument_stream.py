import click

from candlestick.dependency_container import Application


@click.command()
@click.pass_obj
def subscribe_instrument_stream(app: Application):
    click.echo("Start client to handle instrument stream ...")

    app.subscribe_instrument_stream()
