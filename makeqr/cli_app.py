import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Type

import click
from click.decorators import FC
from pydantic import BaseModel, ValidationError

from makeqr import (
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


class FieldExtraClickOptionsModel(BaseModel, arbitrary_types_allowed=True):
    click_option_type: click.types.ParamType = click.types.STRING
    click_option_multiple: bool = False


def make_command_name(
    model_type: Type[QRDataModelType],
) -> str:
    command_name = model_type.__name__.lower().split("model")[0]
    return command_name.lower().split("qr")[1]


def _echo_qr(
    verbose: bool,
    qr: MakeQR,
) -> None:
    matrix = qr.matrix
    if verbose:
        click.echo(click.style("Result".upper(), bold=True))
    for row in matrix:
        for col in row:
            click.echo("██" if col is True else "  ", nl=False)
        click.echo(nl=True)


def _make_click_options_from_model(
    model_cls: Type[QRDataModelType],
) -> List[Callable[[FC], FC]]:
    options = []
    fields = model_cls.__fields__

    if len(fields) == 1:
        name = list(fields.keys())[0]
        model_field = fields[name]
        click_extras = FieldExtraClickOptionsModel.parse_obj(
            model_field.field_info.extra
        )
        options.append(
            click.argument(
                name,
                type=click_extras.click_option_type,
                default=model_field.default,
                required=model_field.required,
            )
        )
        return options

    for name, model_field in model_cls.__fields__.items():
        click_extras = FieldExtraClickOptionsModel.parse_obj(
            model_field.field_info.extra
        )
        option_help = (
            model_field.field_info.description or model_field.name.capitalize()
        )
        options.append(
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
    options.reverse()
    return options


def _echo(
    verbose: bool,
    title: str,
    message: str,
    **kwargs: Any,
) -> None:
    if verbose is True:
        click.echo(click.style(title.upper(), bold=True))
        click.echo(f"  {message}", **kwargs)


def _add_qr_model_command(
    group: click.Group,
    model_cls: Type[QRDataModelType],
) -> None:
    command_name = make_command_name(model_cls)
    options = _make_click_options_from_model(model_cls)

    def func(
        group_params: Dict[str, Any],
        **kwargs: Any,
    ) -> None:
        verbose = group_params["verbose"]
        try:
            model: QRDataModelType = model_cls(**kwargs)
        except ValidationError as err:
            _echo(verbose, "error", str(err), color=True, err=True)
            sys.exit(1)
        _echo(verbose, "Data model", model.json())
        _echo(verbose, "Encoded QR data", model.qr_data)
        qr = MakeQR(
            model,
            box_size=group_params["box-size"],
            border=group_params["border"],
            error_correction=group_params["error-correction"],
        )
        if group_params["print"]:
            _echo_qr(verbose, qr)

        filename = group_params["output"]
        if filename is None:
            return
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
            _echo(verbose, "error", str(err), color=True, err=True)
            sys.exit(1)
        _echo(verbose, "Name of output file", filename)

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
    "--quite",
    "-q",
    is_flag=True,
    default=False,
    show_default=True,
)
@click.option(
    "--print",
    "-p",
    is_flag=True,
    default=False,
    show_default=True,
)
@click.pass_context
def cli_group(
    ctx: click.Context,
    box_size: int,
    border: int,
    error_correction: str,
    output: Optional[str],
    quite: bool,
    print: bool,  # pylint: disable=redefined-builtin
) -> None:
    ctx.obj = {
        "box-size": box_size,
        "border": border,
        "output": output,
        "error-correction": ErrorCorrectionLevel(error_correction),
        "verbose": not quite,
        "print": print,
    }


def make_app() -> click.Group:
    _add_commands(cli_group)
    return cli_group
