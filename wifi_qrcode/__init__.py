from enum import Enum, unique, auto
from typing import Optional, Union, Dict, List, Tuple
from urllib.parse import quote

import qrcode
from qrcode.image.pil import PilImage
from qrcode.image.svg import SvgImage

MECARD_SPECIAL_CHARACTERS: str = '\;,:"'


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
class DataType(Enum):
    WIFI = 'WIFI'
    MAILTO = 'mailto'
    # TEL = 'tel'
    # SMS = 'sms'
    # GEO = 'geo'
    # FACETIME = 'facetime'
    # FACETIME_AUDIO = 'facetime-audio'
    # MARKET = 'market'


def make_mecard_data(title: str, fields: Dict[WifiMecardParam, str]) -> str:

    fields_list = list()

    for field, value in fields.items():
        fields_list.append(f'{field.value}:{value}')

    mecard_data = f'{title}:{";".join(fields_list)};;'

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

    wifi_data = make_mecard_data(title=DataType.WIFI.value, fields=fields)

    return wifi_data


def make_mailto_data(to: str,
                     subject: Optional[str] = None,
                     cc: Optional[Union[List[str], str]] = None,
                     bcc: Optional[Union[List[str], str]] = None,
                     body: Optional[str] = None) -> str:

    data = f'{DataType.MAILTO.value}:{to}'
    args = list()

    if subject:
        args.append(f'subject={quote(subject)}')

    if cc:
        args.append(f'cc={quote(",".join(cc))}')

    if bcc:
        args.append(f'bcc={quote(",".join(bcc))}')

    if body:
        args.append(f'body={quote(body)}')

    if args:
        data = f'{data}?{"&".join(args)}'

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
