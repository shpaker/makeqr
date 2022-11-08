from typer import Typer
from typer.models import CommandInfo
import click
from makeqr.cli_app.handlers.geo import geo_handler

_QR_FILL_COLOR: str = "black"
_QR_BACK_COLOR: str = "white"


def _registered_commands(
    app: Typer,
) -> None:
    app.registered_commands += [
        CommandInfo("geo", callback=geo_handler),
    ]


def make_app() -> click.Group:
    group = click.group()
    cli_group = group(lambda: ...)
    func = geo_handler
    options = (
        click.option('--bar', is_flag=True),
        click.option('--baz', is_flag=True),
    )
    for option in options:
        func = option(func)
    command_decorator = cli_group.command()
    command_decorator(func)
    return cli_group
