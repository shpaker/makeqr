from pathlib import Path
from typing import Callable

from typer.models import CommandInfo

from makeqr import MakeQR
from makeqr.cli_app.constants import DEFAULT_OUTPUT_OPTION
from makeqr.models import GeoModel


def command_wrapper(
    name: str,
):
    output: Path = DEFAULT_OUTPUT_OPTION

    def _wrapper(
        func: Callable,
    ):
        return

    return CommandInfo(name, callback=_wrapper)


@command_wrapper("geo")
def geo_handler(
    latitude: float,
    longitude: float,
    output: Path = DEFAULT_OUTPUT_OPTION,
) -> None:
    qr = MakeQR(
        GeoModel(
            latitude=latitude,
            longitude=longitude,
        )
    )
    qr.save(output)
