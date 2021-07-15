from enum import Enum, unique
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.parse import quote

import qrcode  # pylint: disable=import-error
from qrcode.image.pil import PilImage  # pylint: disable=import-error
from qrcode.image.svg import SvgImage  # pylint: disable=import-error


class AuthType(str, Enum):
    WPA = "wpa"
    WPA2 = "wpa2"
    WEP = "wep"
    NOPASS = "nopass"


@unique
class ImageType(str, Enum):
    SVG = ".svg"
    PNG = ".png"


@unique
class WifiMecardParam(str, Enum):
    HIDDEN = "H"
    SSID = "S"
    AUTH = "T"
    PASSWORD = "P"


@unique
class DataScheme(str, Enum):
    WIFI = "WIFI"
    MAILTO = "mailto"
    TEL = "tel"
    SMS = "sms"
    GEO = "geo"


def make_mecard_data(
    title: str,
    fields: Dict[WifiMecardParam, str],
) -> str:
    fields_list = list()
    for field, value in fields.items():
        fields_list.append(f"{field.value}:{value}")
    mecard_data = f'{title}:{";".join(fields_list)};;'
    return mecard_data


def make_link_data(
    schema: Optional[DataScheme] = None,
    link: Optional[Union[List[str], str]] = None,
    params: Optional[Dict[str, Union[str, str]]] = None,
) -> str:
    if isinstance(link, str):
        link = [link]
    if not link:
        link = list()
    link_str = ",".join(link)
    data = link_str
    if schema:
        data = f"{schema.value}:{data}"
    if params:
        params = {str(param): quote(str(params[param])) for param in params}
        concatenation_char = "&" if "?" in link_str else "?"
        params_list = [f"{param}={value}" for param, value in params.items()]
        params_string = "&".join(params_list)
        data = f"{data}{concatenation_char}{params_string}"
    return data


def make_image(
    data: str,
    file_type: ImageType,
    **kwargs: Any,
) -> Union[PilImage, SvgImage]:
    image_factory = None if file_type is ImageType.PNG else qrcode.image.svg.SvgImage
    qrcode_data = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    qrcode_data.add_data(data)
    qrcode_data.make(fit=True)
    return qrcode_data.make_image(image_factory=image_factory, **kwargs)


def check_file_name(
    file_path: Path,
) -> Tuple[Path, ImageType]:
    try:
        file_type = ImageType(file_path.suffix)
    except KeyError:
        file_type = ImageType.PNG
        file_path = Path(f"{file_path}{file_type}")
    return file_path, file_type


def save_data(
    file_path: Path,
    img: Union[PilImage, SvgImage],
) -> None:
    with open(file_path, "wb") as file:
        img.save(file)
