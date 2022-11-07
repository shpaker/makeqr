from typer import Option

_DEFAULT_OUTPUT_FILENAME = "qrcode.png"

DEFAULT_OUTPUT_OPTION = Option(
    _DEFAULT_OUTPUT_FILENAME,
    exists=False,
    dir_okay=False,
    file_okay=True,
)
