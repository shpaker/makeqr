from enum import Enum, unique, auto
from typing import Optional, Union, Dict

import qrcode
from qrcode.image.pil import PilImage
from qrcode.image.svg import SvgImage


class AuthType(Enum):
    WPA = 'WPA'
    WPA2 = 'WPA'
    WEP = 'WEP'
    nopass = 'nopass'


@unique
class FileFormat(Enum):
    SVG = auto()
    PNG = auto()


@unique
class WifiMecardParam(Enum):
    HIDDEN = 'H'
    SSID = 'S'
    AUTH = 'T'
    PASSWORD = 'P'


QR_FILL_COLOR: str = 'black'
QR_BACK_COLOR: str = 'white'
MECARD_SPECIAL_CHARACTERS: str = '\;,:"'


def make_mecard_data(title: str,
                     fields: Dict[WifiMecardParam, str],
                     end='') -> str:

    fields_list = list()

    for field, value in fields.items():
        fields_list.append(f'{field.value}:{value}')

    mecard_data = f'{title}:{";".join(fields_list)}{end}'

    return mecard_data


def make_wifi_data(ssid: Union[str, int],
                   auth: AuthType = AuthType.nopass,
                   password: Optional[Union[str, int]] = None,
                   hidden: bool = False) -> str:

    if not isinstance(ssid, str):
        ssid = str(ssid)

    if password and not isinstance(password, str):
        password = str(password)

    for spec_char in MECARD_SPECIAL_CHARACTERS:
        ssid = ssid.replace(spec_char, f'\\{spec_char}')
        if password:
            password = password.replace(spec_char, f'\\{spec_char}')

    fields = {WifiMecardParam.AUTH: auth.value, WifiMecardParam.SSID: ssid}

    if hidden:
        fields[WifiMecardParam.HIDDEN] = 'true'

    if auth is not AuthType.nopass and password:
        fields[WifiMecardParam.PASSWORD] = password

    wifi_data = make_mecard_data(title='WIFI', fields=fields, end=';;')

    return wifi_data


def make_image(data: str, file_format: FileFormat, **kwargs) -> PilImage:

    image_factory = None if file_format is FileFormat.PNG else qrcode.image.svg.SvgImage

    qrcode_data = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H)
    qrcode_data.add_data(data)
    qrcode_data.make(fit=True)

    img = qrcode_data.make_image(image_factory=image_factory, **kwargs)

    return img


def save_wifi_qrcode(ssid: str, auth: AuthType, password: Optional[str],
                     hidden: bool, file_format: FileFormat,
                     file_path: str) -> None:

    wifi_data = make_wifi_data(ssid=ssid,
                               auth=auth,
                               password=password,
                               hidden=hidden)

    img = make_image(data=wifi_data,
                     file_format=file_format,
                     fill_color=QR_FILL_COLOR,
                     back_color=QR_BACK_COLOR)

    with open(file_path, 'wb') as file:
        img.save(file)
