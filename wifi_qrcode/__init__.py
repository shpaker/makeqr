from enum import Enum, unique, auto
from typing import Optional

import qrcode
from qrcode.image.svg import SvgImage


@unique
class AuthType(Enum):
    WPA = auto()
    WEP = auto()
    nopass = auto()


@unique
class FileFormat(Enum):
    SVG = auto()
    PNG = auto()


QR_FILL_COLOR: str = 'black'
QR_BACK_COLOR: str = 'white'
MECARD_SPECIAL_CHARACTERS: str = '\;,:"'


def make_wifi_mecard_data(ssid: str,
                          auth: AuthType = AuthType.nopass,
                          password: Optional[str] = None,
                          hidden: bool = False) -> str:

    for spec_char in MECARD_SPECIAL_CHARACTERS:
        ssid = ssid.replace(spec_char, f'\\{spec_char}')
        if password:
            password = password.replace(spec_char, f'\\{spec_char}')

    hidden_part = f';H:true' if hidden else ''
    password_part = f';P:{password}' if auth is not AuthType.nopass and password else ''

    return f'WIFI:T:{auth.name};S:{ssid}{password_part}{hidden_part};;'


def save_wifi_qrcode(ssid: str, auth: AuthType, password: Optional[str],
                     hidden: bool, file_format: FileFormat,
                     file_path: str) -> None:

    image_factory = None if file_format is FileFormat.PNG else qrcode.image.svg.SvgImage

    wifi_data = make_wifi_mecard_data(ssid=ssid,
                                      auth=auth,
                                      password=password,
                                      hidden=hidden)

    qrcode_data = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H)
    qrcode_data.add_data(wifi_data)
    qrcode_data.make(fit=True)

    img = qrcode_data.make_image(fill_color=QR_FILL_COLOR,
                                 back_color=QR_BACK_COLOR,
                                 image_factory=image_factory)

    with open(file_path, 'wb') as file:
        img.save(file)
