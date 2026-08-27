import types as pytypes
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Union, get_args, get_origin

import click
from pydantic import SecretStr, ValidationError
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined

from makeqr import (
    QRDataModel,
    __version__,
)
from makeqr.constants import DEFAULT_IMAGE_FORMAT, ErrorCorrectionLevel
from makeqr.makeqr import MakeQR

#: A click decorator factory such as ``click.option(...)``.
_Decorator = Callable[[Any], Any]

_CAPTION = (
    " __   __  _______  ___   _  _______  _______  ______\n"
    "|  |_|  ||   _   ||   | | ||       ||       ||    _ |\n"
    "|       ||  |_|  ||   |_| ||    ___||   _   ||   | ||\n"
    "|       ||       ||      _||   |___ |  | |  ||   |_||_\n"
    "|       ||       ||     |_ |    ___||  |_|  ||    __  |\n"
    "| ||_|| ||   _   ||    _  ||   |___ |      | |   |  | |\n"
    "|_|   |_||__| |__||___| |_||_______||____||_||___|  |_|\n"
)


@dataclass(frozen=True)
class GroupOptions:
    box_size: int
    border: int
    error_correction: ErrorCorrectionLevel
    output: str | None
    verbose: bool
    quiet: bool


@dataclass(frozen=True)
class _ParamSpec:
    """How a model field should be exposed on the command line."""

    param_type: click.types.ParamType
    multiple: bool
    is_flag: bool


def _qr_models() -> tuple[type[QRDataModel], ...]:
    return tuple(sorted(QRDataModel.__subclasses__(), key=lambda model: model.__name__))


def _make_command_name(
    model_type: type[QRDataModel],
) -> str:
    command_name = model_type.__name__.lower().split("model")[0]
    return command_name.lower().split("qr")[1]


def _unwrap_optional(annotation: Any) -> Any:
    origin = get_origin(annotation)
    if origin is Union or origin is pytypes.UnionType:
        args = [arg for arg in get_args(annotation) if arg is not type(None)]
        if len(args) == 1:
            return args[0]
    return annotation


def _param_spec(
    field: FieldInfo,
) -> _ParamSpec:
    """Derive the click parameter shape from the field's own annotation."""
    annotation = _unwrap_optional(field.annotation)
    multiple = False

    if get_origin(annotation) is tuple:
        multiple = True
        args = [arg for arg in get_args(annotation) if arg is not Ellipsis]
        annotation = _unwrap_optional(args[0]) if args else str

    if annotation is bool:
        return _ParamSpec(click.types.BOOL, multiple=multiple, is_flag=True)
    if annotation is float:
        return _ParamSpec(click.types.FLOAT, multiple=multiple, is_flag=False)
    if annotation is int:
        return _ParamSpec(click.types.INT, multiple=multiple, is_flag=False)
    if isinstance(annotation, type) and issubclass(annotation, Enum):
        choice = click.types.Choice(
            [str(member.value) for member in annotation],
            case_sensitive=False,
        )
        return _ParamSpec(choice, multiple=multiple, is_flag=False)
    return _ParamSpec(click.types.STRING, multiple=multiple, is_flag=False)


def _get_from_model_argument_name(
    model_cls: type[QRDataModel],
) -> str | None:
    """Return the field to expose as a positional argument, if exactly one fits."""
    argument_name = None
    for name, model_field in model_cls.model_fields.items():
        spec = _param_spec(model_field)
        if model_field.is_required() and not spec.multiple:
            if argument_name is not None:
                return None
            argument_name = name
    return argument_name


def _field_default(
    model_field: FieldInfo,
) -> Any:
    default = model_field.default
    if default is PydanticUndefined:
        return None
    return default.value if isinstance(default, Enum) else default


def _make_click_options_from_model(
    model_cls: type[QRDataModel],
) -> list[_Decorator]:
    params: list[_Decorator] = []
    argument_name = _get_from_model_argument_name(model_cls)

    for name, model_field in model_cls.model_fields.items():
        spec = _param_spec(model_field)

        if argument_name == name:
            params.append(
                click.argument(
                    name,
                    type=spec.param_type,
                    default=_field_default(model_field),
                    required=model_field.is_required(),
                )
            )
            continue

        # A short flag needs an alias to derive its name from; long-only is
        # better than the "-None" a missing alias used to produce.
        names = [f"--{name}"]
        if model_field.alias:
            names.insert(0, f"-{model_field.alias}")

        option_kwargs: dict[str, Any] = {
            "default": _field_default(model_field),
            "required": model_field.is_required(),
            "help": model_field.description or name.capitalize(),
            "multiple": spec.multiple,
        }
        if spec.is_flag:
            option_kwargs["is_flag"] = True
        else:
            option_kwargs["type"] = spec.param_type
            option_kwargs["show_default"] = True

        params.append(click.option(*names, **option_kwargs))

    params.reverse()
    return params


def _echo(
    message: str,
    verbose: bool = True,
    **kwargs: Any,
) -> None:
    if verbose:
        click.echo(message, **kwargs)


def _echo_qr(
    qr: MakeQR,
) -> None:
    for row in qr.matrix:
        click.echo("".join("██" if col else "  " for col in row))


def _save_file(
    qr: MakeQR,
    filename: str | Path,
    verbose: bool,
) -> None:
    path = Path(filename)
    try:
        qr.save(path)
    except ValueError:
        # No usable extension: fall back to a sibling PNG rather than clobbering
        # whatever the user already has at that path.
        path = path.with_name(f"{path.name}.{DEFAULT_IMAGE_FORMAT}")
        try:
            qr.save(path)
        except OSError as err:
            raise click.ClickException(str(err)) from err
    except OSError as err:
        raise click.ClickException(str(err)) from err
    _echo(f"Output: {path}", verbose=verbose)


def _add_qr_model_command(
    group: click.Group,
    model_cls: type[QRDataModel],
) -> None:
    command_name = _make_command_name(model_cls)
    options = _make_click_options_from_model(model_cls)

    def func(
        group_options: GroupOptions,
        **kwargs: Any,
    ) -> None:
        verbose = group_options.verbose
        _echo(click.style(_CAPTION, bold=True), verbose=verbose)
        try:
            model = model_cls(**kwargs)
        except ValidationError as err:
            raise click.ClickException(str(err)) from err
        if verbose:
            _echo(f"Model: {model.model_dump_json()}")
            _echo(f"Encoded: {_redact(model)}")
        qr = MakeQR(
            model,
            box_size=group_options.box_size,
            border=group_options.border,
            error_correction=group_options.error_correction,
        )
        if group_options.output is not None:
            _save_file(qr, group_options.output, verbose)
        if not group_options.quiet:
            _echo_qr(qr)

    func.__doc__ = f"Encode {command_name} data."
    command: Any = func
    for option in options:
        command = option(command)
    group.command(name=command_name)(click.pass_obj(command))


def _redact(
    model: QRDataModel,
) -> str:
    """Payload with secret values masked, for the verbose log.

    The mask is substituted before the payload is built, so it survives whatever
    escaping the model applies to the real value.
    """
    masked = {
        name: SecretStr("***") for name in type(model).model_fields if isinstance(getattr(model, name, None), SecretStr)
    }
    if not masked:
        return model.qr_data
    return model.model_copy(update=masked).qr_data


def _add_commands(
    group: click.Group,
) -> None:
    for model in _qr_models():
        _add_qr_model_command(group, model)


def _echo_version(
    ctx: click.Context,
    param: click.Parameter,
    value: bool,
) -> None:
    if not value or ctx.resilient_parsing:
        return
    click.echo(__version__)
    ctx.exit()


@click.group()
@click.option(
    "--box-size",
    "-s",
    type=click.INT,
    default=8,
    show_default=True,
    help="Pixel size of a single QR module.",
)
@click.option(
    "--border",
    "-b",
    type=click.INT,
    default=1,
    show_default=True,
    help="Width of the quiet zone, in modules.",
)
@click.option(
    "--error-correction",
    "-e",
    type=click.Choice(ErrorCorrectionLevel.get_values()),
    default=ErrorCorrectionLevel.MEDIUM.value,
    show_default=True,
    help="How much of the code can be damaged and still scan.",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    default=None,
    help="Write the image here. The extension picks the format.",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    default=False,
    help="Print the model and the encoded payload.",
)
@click.option(
    "--quiet",
    "--quite",
    "-q",
    "quiet",
    is_flag=True,
    default=False,
    help="Do not print the QR code to the terminal.",
)
@click.option(
    "--version",
    "-V",
    is_flag=True,
    default=False,
    expose_value=False,
    is_eager=True,
    callback=_echo_version,
    help="Show the version and exit.",
)
@click.pass_context
def cli_group(
    ctx: click.Context,
    box_size: int,
    border: int,
    error_correction: str,
    output: str | None,
    verbose: bool,
    quiet: bool,
) -> None:
    """Generate QR codes for links, WiFi networks, geo points and more.

    Global options go before the command name:

        makeqr -o code.png wifi --security wpa --password s3cret HomeWiFi
    """
    ctx.obj = GroupOptions(
        box_size=box_size,
        border=border,
        error_correction=ErrorCorrectionLevel(error_correction),
        output=output,
        verbose=verbose,
        quiet=quiet,
    )


def make_app() -> click.Group:
    _add_commands(cli_group)
    return cli_group
