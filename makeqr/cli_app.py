import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Type

import click
from click.decorators import FC
from pydantic import BaseModel, ValidationError
from pydantic.fields import ModelField

from makeqr import (
    VERSION,
    MakeQR,
    QRDataModelType,
    QRGeoModel,
    QRLinkModel,
    QRMailToModel,
    QRSMSModel,
    QRTelModel,
    QRTextModel,
    QRWiFiModel,
)
from makeqr.constants import DEFAULT_IMAGE_FORMAT, ErrorCorrectionLevel

_QR_MODELS_LIST = (
    QRGeoModel,
    QRLinkModel,
    QRMailToModel,
    QRSMSModel,
    QRTelModel,
    QRTextModel,
    QRWiFiModel,
)
_CAPTION = (
    " __   __  _______  ___   _  _______  _______  ______\n"
    "|  |_|  ||   _   ||   | | ||       ||       ||    _ |\n"
    "|       ||  |_|  ||   |_| ||    ___||   _   ||   | ||\n"
    "|       ||       ||      _||   |___ |  | |  ||   |_||_\n"
    "|       ||       ||     |_ |    ___||  |_|  ||    __  |\n"
    "| ||_|| ||   _   ||    _  ||   |___ |      | |   |  | |\n"
    "|_|   |_||__| |__||___| |_||_______||____||_||___|  |_|\n"
)


class FieldExtraClickOptionsModel(
    BaseModel,
    arbitrary_types_allowed=True,
):
    click_option_type: click.types.ParamType = click.types.STRING
    click_option_multiple: bool = False


def _make_command_name(
    model_type: Type[QRDataModelType],
) -> str:
    command_name = model_type.__name__.lower().split("model")[0]
    return command_name.lower().split("qr")[1]


def _get_from_model_argument_name(
    model_cls: Type[QRDataModelType],
) -> Any:
    argument_name = None
    for name, model_field in model_cls.__fields__.items():
        click_extras = FieldExtraClickOptionsModel.parse_obj(
            model_field.field_info.extra
        )
        model_field: ModelField
        if model_field.required is True and click_extras.click_option_multiple is False:
            if argument_name is not None:
                return None
            argument_name = name
    return argument_name


def _echo_qr(
    qr: MakeQR,
) -> None:
    for row in qr.matrix:
        for col in row:
            click.echo("██" if col is True else "  ", nl=False)
        click.echo(nl=True)


def _make_click_argument(
    name: str,
    model_field: ModelField,
) -> Callable:
    click_extras = FieldExtraClickOptionsModel.parse_obj(
        model_field.field_info.extra
    )
    return click.argument(
        name,
        type=click_extras.click_option_type,
        default=model_field.default,
        required=model_field.required,
    )


def _make_click_options_from_model(
    model_cls: Type[QRDataModelType],
) -> List[Callable[[FC], FC]]:
    params = []
    argument_name = _get_from_model_argument_name(model_cls)

    for name, model_field in model_cls.__fields__.items():

        if argument_name == name:
            click_extras = FieldExtraClickOptionsModel.parse_obj(
                model_field.field_info.extra
            )
            params.append(
                click.argument(
                    name,
                    type=click_extras.click_option_type,
                    default=model_field.default,
                    required=model_field.required,
                )
            )
            continue

        click_extras = FieldExtraClickOptionsModel.parse_obj(
            model_field.field_info.extra
        )
        option_help = (
            model_field.field_info.description or model_field.name.capitalize()
        )
        params.append(
            click.option(
                f"-{model_field.alias}",
                f"--{name}",
                type=click_extras.click_option_type,
                default=model_field.default,
                required=model_field.required,
                show_default=True,
                help=option_help,
                multiple=click_extras.click_option_multiple,
            )
        )
    params.reverse()
    return params


def _echo(
    message: str,
    verbose: bool = True,
    **kwargs,
) -> None:
    if verbose is True:
        click.echo(message, **kwargs)


def _save_file(
    qr: MakeQR,
    filename: Path,
    verbose: bool,
) -> None:
    filename = Path(filename)
    is_exist_before = filename.exists()

    try:
        qr.save(filename)
    except ValueError:
        if not is_exist_before:
            try:
                filename.unlink()
            except FileNotFoundError:
                pass
        filename = f"{filename}.{DEFAULT_IMAGE_FORMAT}"
        qr.save(filename)
    except OSError as err:
        _echo(f"ERROR:\n{str(err)}", err=True)
        sys.exit(1)
    _echo(f"Output: {filename}", verbose=verbose)


def _add_qr_model_command(
    group: click.Group,
    model_cls: Type[QRDataModelType],
) -> None:
    command_name = _make_command_name(model_cls)
    options = _make_click_options_from_model(model_cls)

    def func(
        group_params: Dict[str, Any],
        **kwargs: Any,
    ) -> None:
        verbose = group_params["verbose"]
        _echo(click.style(_CAPTION, bold=True), verbose=verbose)
        try:
            model: QRDataModelType = model_cls(**kwargs)
        except ValidationError as err:
            _echo(f"ERROR:\n{str(err)}", err=True)
            sys.exit(1)
        _echo(f"Model: {model.json()}", verbose=verbose)
        _echo(f"Encoded: {model.qr_data}", verbose=verbose)
        qr = MakeQR(
            model,
            box_size=group_params["box-size"],
            border=group_params["border"],
            error_correction=group_params["error-correction"],
        )
        filename = group_params["output"]
        if filename is not None:
            _save_file(qr, filename, verbose)

        if not group_params["quite"]:
            _echo_qr(qr)

    for option in options:
        func = option(func)
    command_decorator = group.command(name=command_name)
    func = click.pass_obj(func)
    command_decorator(func)


def _add_commands(
    group: click.Group,
) -> None:
    for model in _QR_MODELS_LIST:
        _add_qr_model_command(group, model)  # type: ignore


def _echo_version(
    ctx: click.Context,
    param: bool,  # noqa, pylint: disable=unused-argument
    value: str,
) -> None:
    if not value or ctx.resilient_parsing:
        return
    click.echo(VERSION)
    ctx.exit()


@click.group()
@click.option(
    "--box-size",
    "-s",
    type=click.INT,
    default=8,
    show_default=True,
)
@click.option(
    "--border",
    "-b",
    type=click.INT,
    default=1,
    show_default=True,
)
@click.option(
    "--error-correction",
    "-e",
    type=click.Choice(ErrorCorrectionLevel.get_values()),
    default=ErrorCorrectionLevel.MEDIUM.value,
    show_default=True,
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    default=None,
    show_default=True,
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    default=False,
)
@click.option(
    "--quite",
    "-q",
    is_flag=True,
    default=False,
)
@click.option(
    "--print",
    "-p",
    is_flag=True,
    default=False,
)
@click.option(
    "--version",
    "-V",
    is_flag=True,
    default=False,
    expose_value=False,
    is_eager=True,
    callback=_echo_version,
)
@click.pass_context
def cli_group(
    ctx: click.Context,
    box_size: int,
    border: int,
    error_correction: str,
    output: Optional[str],
    verbose: bool,
    quite: bool,
    print: bool,  # noqa, pylint: disable=redefined-builtin
) -> None:
    ctx.obj = {
        "box-size": box_size,
        "border": border,
        "output": output,
        "error-correction": ErrorCorrectionLevel(error_correction),
        "verbose": verbose,
        "quite": quite,
        "print": print,
    }


def make_app() -> click.Group:
    _add_commands(cli_group)
    return cli_group
