from pathlib import Path
from typing import Any, Optional, Type, Union

from pydantic import ValidationError
from typer import Exit, Option, Typer, colors, echo, style

from makeqr.enums import AuthType
from makeqr.models.geo import GeoModel
from makeqr.models.link import LinkModel
from makeqr.models.mailto import MailToModel
from makeqr.models.sms import SmsModel
from makeqr.models.tel import TelModel
from makeqr.models.wifi import WiFiModel
from makeqr.utils import check_file_name, make_image

app = Typer()

DEFAULT_OUTPUT: str = "qrcode.png"
QR_FILL_COLOR: str = "black"
QR_BACK_COLOR: str = "white"


def _save_qr(
    model: Union[
        GeoModel,
        LinkModel,
        MailToModel,
        SmsModel,
        TelModel,
        WiFiModel,
    ],
    filename: Path,
) -> None:
    file_name, file_type = check_file_name(filename)
    prefix = style("OUTPUT\n", fg=colors.GREEN, bold=True)
    echo(prefix + f"  {file_name}")
    prefix = style("FORMAT\n", fg=colors.GREEN, bold=True)
    echo(prefix + f"  {file_type.name}")
    prefix = style("DATA\n", fg=colors.GREEN, bold=True)
    echo(prefix + f"  {model.qr_data}")
    img = make_image(
        data=model.qr_data,
        file_type=file_type,
        fill_color=QR_FILL_COLOR,
        back_color=QR_BACK_COLOR,
    )
    with open(file_name, "wb") as file:
        img.save(file)


def _make_model(
    model_type: Union[
        Type[GeoModel],
        Type[LinkModel],
        Type[MailToModel],
        Type[SmsModel],
        Type[TelModel],
        Type[WiFiModel],
    ],
    **kwargs: Any,
) -> Union[GeoModel, LinkModel, MailToModel, SmsModel, TelModel, WiFiModel]:
    try:
        return model_type(**kwargs)
    except ValidationError as err:
        prefix = style("ERROR:\n", fg=colors.GREEN, bold=True)
        echo(prefix + err)
        raise Exit(code=1) from err


@app.command()
def geo(
    latitude: float,
    longitude: float,
    output: Path = Option(
        DEFAULT_OUTPUT,
        exists=False,
        dir_okay=False,
        file_okay=True,
    ),
) -> None:
    model = _make_model(
        GeoModel,
        latitude=latitude,
        longitude=longitude,
    )
    _save_qr(model, output)


@app.command()
def link(
    url: str,
    output: Path = Option(
        DEFAULT_OUTPUT,
        exists=False,
        dir_okay=False,
        file_okay=True,
    ),
) -> None:
    model = _make_model(
        LinkModel,
        url=url,
    )
    _save_qr(model, output)


@app.command()
def mailto(
    to: str,
    subject: Optional[str] = None,
    cc: Optional[str] = None,
    bcc: Optional[str] = None,
    body: Optional[str] = None,
    output: Path = Option(
        DEFAULT_OUTPUT,
        exists=False,
        dir_okay=False,
        file_okay=True,
    ),
) -> None:
    cc_list = list()
    bcc_list = list()
    if cc:
        cc_list = cc.split(",")
    if bcc:
        bcc_list = bcc.split(",")
    model = _make_model(
        MailToModel,
        to=to,
        subject=subject,
        cc=cc_list,
        bcc=bcc_list,
        body=body,
    )
    _save_qr(model, output)


@app.command()
def sms(
    recipients: str,
    body: Optional[str] = None,
    output: Path = Option(
        DEFAULT_OUTPUT,
        exists=False,
        dir_okay=False,
        file_okay=True,
    ),
) -> None:
    model = _make_model(
        SmsModel,
        recipients=(recipients,),
        body=body,
    )
    _save_qr(model, output)


@app.command()
def tel(
    number: str,
    output: Path = Option(
        DEFAULT_OUTPUT,
        exists=False,
        dir_okay=False,
        file_okay=True,
    ),
) -> None:
    model = _make_model(
        TelModel,
        tel=number,
    )
    _save_qr(model, output)


@app.command()
def wifi(
    ssid: str,
    security: Optional[AuthType] = None,
    password: Optional[str] = None,
    hidden: bool = False,
    output: Path = Option(
        DEFAULT_OUTPUT,
        exists=False,
        dir_okay=False,
        file_okay=True,
    ),
) -> None:
    model = _make_model(
        WiFiModel,
        ssid=ssid,
        security=security,
        password=password,
        hidden=hidden,
    )
    _save_qr(model, output)


def main() -> None:
    app()
