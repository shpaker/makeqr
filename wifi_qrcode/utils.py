from enum import Enum, unique, auto
from typing import Optional, Union, Dict, List
from urllib.parse import quote

import qrcode
from qrcode.image.pil import PilImage
from qrcode.image.svg import SvgImage


class AuthType(Enum):
    WPA = 'WPA'
    WPA2 = 'WPA'
    WEP = 'WEP'
    nopass = 'nopass'


@unique
class ImageFormat(Enum):
    SVG = auto()
    PNG = auto()


@unique
class WifiMecardParam(Enum):
    HIDDEN = 'H'
    SSID = 'S'
    AUTH = 'T'
    PASSWORD = 'P'


@unique
class DataScheme(Enum):
    WIFI = 'WIFI'
    MAILTO = 'mailto'
    TEL = 'tel'
    SMS = 'sms'
    GEO = 'geo'


def make_mecard_data(title: str, fields: Dict[WifiMecardParam, str]) -> str:

    fields_list = list()

    for field, value in fields.items():
        fields_list.append(f'{field.value}:{value}')

    mecard_data = f'{title}:{";".join(fields_list)};;'

    return mecard_data


def make_link_data(schema: Optional[DataScheme] = None,
                   link: Optional[Union[List[str], str]] = None,
                   params: Optional[Dict[str, str]] = None) -> str:

    if isinstance(link, str):
        link = [link]

    if not link:
        link = list()

    link_str = ','.join(link)
    data = link_str

    if schema:
        data = f'{schema.value}:{data}'

    if params:
        params = {str(param): quote(str(params[param])) for param in params}
        concatenation_char = '&' if '?' in link_str else '?'
        params_list = [f'{param}={value}' for param, value in params.items()]
        params_string = '&'.join(params_list)
        data = f'{data}{concatenation_char}{params_string}'

    return data


def make_image(data: str, file_format: ImageFormat,
               **kwargs) -> Union[PilImage, SvgImage]:

    image_factory = None if file_format is ImageFormat.PNG else qrcode.image.svg.SvgImage

    qrcode_data = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H)
    qrcode_data.add_data(data)
    qrcode_data.make(fit=True)

    img = qrcode_data.make_image(image_factory=image_factory, **kwargs)

    return img
