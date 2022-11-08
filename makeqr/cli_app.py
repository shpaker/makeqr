from enum import Enum
from typing import Type, TypeVar, Any, Generic

import click
from pydantic import ValidationError
from pydantic.fields import Undefined, ModelField

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


class TypeClickMapping(Enum):
    STR = click.STRING
    INT = click.INT
    FLOAT = click.FLOAT
    BOOL = click.BOOL
    ENUM = click.Choice


class TypePyMapping(Enum):
    INT = int
    FLOAT = float
    BOOL = bool
    ENUM = Enum


def _is_enum(
    py_type: Type[Any],
) -> bool:
    try:
        return issubclass(py_type, Enum)
    except TypeError:
        return False


def _is_tuple(
    py_type: ModelField,
) -> bool:
    try:
        return py_type.outer_type_.__origin__ in [tuple, list]
    except AttributeError:
        return False


def _py_to_click_types(
    py_type: ModelField,
):
    if _is_enum(py_type.type_):
        return click.Choice(choices=[entry.value for entry in py_type.type_])
    if _is_tuple(py_type):
        return click.Tuple([click.STRING])
    try:
        _type_in_mapping = TypePyMapping(py_type)
    except ValueError:
        return TypeClickMapping.STR.value
    return TypeClickMapping[_type_in_mapping.name].value


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
            # todo: echo error
            raise
        qr = MakeQR(model)
        qr.save('test.jpeg')

    func = _wrapper

    options = (
        click.option(
            f'--{name}',
            type=_py_to_click_types(model_field),
            default=model_field.default,
            required=model_field.required,
            show_default=True,
            help=model_field.field_info.description,
        )
        for name, model_field in reversed(fields.items())
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
