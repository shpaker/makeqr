from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.parse import quote

import qrcode
from qrcode.image.pil import PilImage
from qrcode.image.svg import SvgImage

from makeqr.enums import DataScheme, ImageType, WifiMecardParam


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
    params: Optional[Dict[str, Any]] = None,
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
    image_factory = (
        None if file_type is ImageType.PNG else qrcode.image.svg.SvgImage
    )
    qrcode_data = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=0,
    )
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
    return file_path.resolve(), file_type
