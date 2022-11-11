import sys
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
from makeqr.cli_app.field_extra import FieldExtraClickOptionsModel

_QR_MODELS_LIST = (
    QRGeoModel,
    QRLinkModel,
    QRMailToModel,
    QRSMSModel,
    QRTelModel,
    QRTextModel,
    QRWiFiModel,
)


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
                f"--{name}",
                f"-{model_field.alias}",
                type=click_extras.click_option_type,
                default=model_field.default,
                required=model_field.required,
                show_default=True,
                help=option_help,
                multiple=click_extras.click_option_multiple,
            )
        )

    def _wrapper(
        **kwargs: Any,
    ) -> None:
        try:
            model = model_type(**kwargs)
        except ValidationError as err:
            click.echo(err, color=True)
            sys.exit(1)
        click.echo(model.qr_data)
        qr = MakeQR(model)
        qr.save("test.jpeg")

    func = _wrapper

    for option in options:
        func = option(func)
    command_decorator = cli_group.command(
        name=command_name,
        context_settings={
            "ignore_unknown_options": True,
            "allow_extra_args": True,
        },
    )
    func = command_decorator(func)
    click.pass_context(func)


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
