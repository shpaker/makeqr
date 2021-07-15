from pathlib import Path
from typing import Optional

from typer import Option

from makeqr import makers
from makeqr.app import app, main
from makeqr.utils import AuthType, check_file_name, make_image, save_data

DEFAULT_OUTPUT: str = "qrcode.png"

QR_FILL_COLOR: str = "black"
QR_BACK_COLOR: str = "white"


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
    file_name, file_type = check_file_name(output)
    data = makers.make_geo(
        latitude=latitude,
        longitude=longitude,
    )
    img = make_image(
        data=data,
        file_type=file_type,
        fill_color=QR_FILL_COLOR,
        back_color=QR_BACK_COLOR,
    )
    save_data(file_name, img)


def link(
    url: str,
    output: Path = Option(
        DEFAULT_OUTPUT,
        exists=False,
        dir_okay=False,
        file_okay=True,
    ),
) -> None:
    file_name, file_type = check_file_name(output)
    data = makers.make_link(url=url)
    img = make_image(
        data=data,
        file_type=file_type,
        fill_color=QR_FILL_COLOR,
        back_color=QR_BACK_COLOR,
    )
    save_data(file_name, img)


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
    file_name, file_type = check_file_name(output)
    cc_list = list()
    bcc_list = list()
    if cc:
        cc_list = cc.split(",")
    if bcc:
        bcc_list = bcc.split(",")
    data = makers.make_mailto(
        to=to,
        subject=subject,
        cc=cc_list,
        bcc=bcc_list,
        body=body,
    )
    img = make_image(
        data=data,
        file_type=file_type,
        fill_color=QR_FILL_COLOR,
        back_color=QR_BACK_COLOR,
    )
    save_data(file_name, img)


@app.command()
def wifi(
    ssid: str,
    auth: AuthType = Option(AuthType.WPA),
    password: Optional[str] = None,
    hidden: bool = False,
    output: Path = Option(
        DEFAULT_OUTPUT,
        exists=False,
        dir_okay=False,
        file_okay=True,
    ),
) -> None:
    file_name, file_type = check_file_name(output)
    data = makers.make_wifi(
        ssid=ssid,
        auth=auth,
        password=password,
        hidden=hidden,
    )
    img = make_image(
        data=data,
        file_type=file_type,
        fill_color=QR_FILL_COLOR,
        back_color=QR_BACK_COLOR,
    )
    save_data(file_name, img)


if __name__ == "__main__":
    main()
