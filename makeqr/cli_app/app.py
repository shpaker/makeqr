from typer import Typer
from typer.models import CommandInfo

from makeqr.cli_app.handlers.geo import geo_handler

_QR_FILL_COLOR: str = "black"
_QR_BACK_COLOR: str = "white"


def _registered_commands(
    app: Typer,
) -> None:
    app.registered_commands += [
        CommandInfo("geo", callback=geo_handler),
    ]


def make_app() -> Typer:
    app = Typer()
    _registered_commands(app)
    return app
