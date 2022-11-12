import sys
from typing import Any, Callable, Dict, List, Type

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


# def echo_qr(qr: MakeQR) -> None:
#     for row in qr.matrix:
#         for col in row:
#             _echo("██" if col is True else "  ", nl=False)
#         _echo(nl=True)


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
    group_params: Dict[str, Any],
    title: str,
    message: str,
    **kwargs: Any,
) -> None:
    verbose = group_params["verbose"]
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
        try:
            model: QRDataModelType = model_cls(**kwargs)
        except ValidationError as err:
            _echo(group_params, "error", str(err), color=True, err=True)
            sys.exit(1)
        _echo(group_params, "Data model", model.json())
        _echo(group_params, "Encoded QR data", model.qr_data)
        qr = MakeQR(
            model,
            box_size=group_params["box-size"],
            border=group_params["border"],
            error_correction=group_params["error-correction"],
        )

        filename = group_params["output"]
        try:
            qr.save(filename)
        except ValueError:
            filename = f"{filename}.{DEFAULT_IMAGE_FORMAT}"
            qr.save(filename, format=DEFAULT_IMAGE_FORMAT)
        except OSError as err:
            _echo(group_params, "error", str(err), color=True, err=True)
            sys.exit(1)
        _echo(group_params, "Name of output file", filename)

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
    default="output.png",
    show_default=True,
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    default=False,
    show_default=True,
)
@click.pass_context
def cli_group(
    ctx: click.Context,
    box_size: int,
    border: int,
    output: str,
    verbose: bool,
    error_correction: str,
) -> None:
    ctx.obj = {
        "box-size": box_size,
        "border": border,
        "output": output,
        "error-correction": ErrorCorrectionLevel(error_correction),
        "verbose": verbose,
    }


def make_app() -> click.Group:
    _add_commands(cli_group)
    return cli_group
