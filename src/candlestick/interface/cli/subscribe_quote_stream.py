import click

from candlestick.dependency_container import Application


@click.command()
@click.pass_obj
def subscribe_quote_stream(app: Application):
    click.echo("Start client to handle quote stream ...")

    app.subscribe_quote_stream()
