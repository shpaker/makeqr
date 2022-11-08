from typing import Type, TypeVar, Any

import click
from pydantic import ValidationError

from makeqr import MakeQR
from makeqr.base import QrDataBaseModel
from makeqr.models import *  # noqa

QR_MODELS_LIST = (
    GeoModel,
    LinkModel,
    MailToModel,
    SmsModel,
    TelModel,
    WiFiModel,
)
T = TypeVar("T", bound=QrDataBaseModel)


def _add_qr_model_command(
    cli_group: click.Group,
    model_type: Type[T],
):
    command_name = model_type.__name__.lower().split('model')[0]
    fields = model_type.__fields__

    def _wrapper(
        **kwargs: Any,
    ) -> None:
        try:
            model = model_type(**kwargs)
        except ValidationError:
            click.echo
        qr = MakeQR(model)
        qr.save('test.jpeg')

    func = _wrapper

    options = (
        click.option(
            f'--{name}',
            # todo: describe types (pydantic -> click)
            default=meta.default,
            show_default=True,
            help=meta.field_info.description,
        )
        for name, meta in reversed(fields.items())
    )
    for option in options:
        func = option(func)
    command_decorator = cli_group.command(name=command_name)
    command_decorator(func)


def _add_commands(
    cli_group: click.Group,
):
    for model in QR_MODELS_LIST:
        _add_qr_model_command(cli_group, model)


def make_app() -> click.Group:
    group_decorator = click.group()
    cli_group = group_decorator(lambda: ...)

    _add_commands(cli_group)

    return cli_group
