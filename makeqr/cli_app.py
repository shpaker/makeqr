import sys
from typing import Any, Callable, Dict, List, Type

import click
from click.decorators import FC
from pydantic import BaseModel, ValidationError

from makeqr import (
    MakeQR,
    QRDataModel,
    QRGeoModel,
    QRLinkModel,
    QRMailToModel,
    QRSMSModel,
    QRTelModel,
    QRTextModel,
    QRWiFiModel,
)

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
    model_type: Type[QRDataModel],
) -> str:
    command_name = model_type.__name__.lower().split("model")[0]
    return command_name.lower().split("qr")[1]


def echo_qr(qr: MakeQR) -> None:
    for row in qr.matrix:
        for col in row:
            click.echo("██" if col is True else "  ", nl=False)
        click.echo(nl=True)


def _make_options_from_model(
    model_cls: Type[QRDataModel],
) -> List[Callable[[FC], FC]]:
    options = []

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


def _add_qr_model_command(
    group: click.Group,
    model_cls: Type[QRDataModel],
) -> None:
    command_name = make_command_name(model_cls)
    options = _make_options_from_model(model_cls)

    def func(
        group_params: Dict[str, Any],
        **kwargs: Any,
    ) -> None:
        try:
            model = model_cls(**kwargs)
        except ValidationError as err:
            click.echo(str(err), color=True, err=True)
            sys.exit(1)
        qr = MakeQR(
            model,
            box_size=group_params["size"],
            border=group_params["border"],
        )

        try:
            qr.save(group_params["output"])
        except ValueError as err:
            click.echo(str(err), color=True, err=True)
            qr.save(f"{group_params['output']}.png")
        except OSError as err:
            click.echo(str(err), color=True, err=True)
            sys.exit(1)

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
@click.option("--size", "-s", type=click.INT, default=8)
@click.option("--border", "-b", type=click.INT, default=6)
@click.option("--output", "-o", type=click.Path(), default="output.png")
@click.pass_context
def cli_group(
    ctx: click.Context,
    size: int,
    border: int,
    output: str,
) -> None:
    ctx.obj = {"size": size, "border": border, "output": output}


def make_app() -> click.Group:
    _add_commands(cli_group)
    return cli_group
