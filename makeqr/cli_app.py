from typing import Any, Type

import click
from pydantic import ValidationError

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
from click import types, Context
from pydantic import BaseModel


class FieldExtraClickOptionsModel(BaseModel, arbitrary_types_allowed=True):
    click_option_type: types.ParamType = types.STRING
    click_option_multiple: bool = False


def _add_qr_model_command(
    cli_group: click.Group,
    model_type: Type[QRDataModel],
) -> None:
    command_name = model_type.__name__.lower().split("model")[0]
    command_name = command_name.lower().split("qr")[1]
    fields = model_type.__fields__
    options = []

    for name, model_field in reversed(fields.items()):
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

    def func(
        ctx: Context,
        **kwargs: Any,
    ) -> None:
        try:
            model = model_type(**kwargs)
        except ValidationError as err:
            click.echo(str(err), color=True, err=True)
            ctx.exit(1)
        click.echo(model.dict())
        qr = MakeQR(model)
        qr.save("output.jpeg")

    for option in options:
        func = option(func)
    command_decorator = cli_group.command(
        name=command_name,
        context_settings={
            "ignore_unknown_options": True,
            "allow_extra_args": True,
        },
    )
    func = click.pass_context(func)
    command_decorator(func)


def _add_commands(
    cli_group: click.Group,
) -> None:
    for model in _QR_MODELS_LIST:
        _add_qr_model_command(cli_group, model)  # type: ignore


def make_app() -> click.Group:
    group_decorator = click.group()
    cli_group = group_decorator(lambda: ...)
    _add_commands(cli_group)
    return cli_group
