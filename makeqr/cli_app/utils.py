from pathlib import Path
from typing import Any, Tuple, Union

import qrcode
from qrcode.image.pil import PilImage
from qrcode.image.svg import SvgImage

from makeqr.enums import ImageFormat


def make_image(
    data: str,
    file_type: ImageFormat,
    **kwargs: Any,
) -> Union[PilImage, SvgImage]:
    image_factory = (
        None if file_type is ImageFormat.PNG else qrcode.image.svg.SvgImage
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
) -> Tuple[Path, ImageFormat]:
    try:
        file_type = ImageFormat(file_path.suffix)
    except KeyError:
        file_type = ImageFormat.PNG
        file_path = Path(f"{file_path}{file_type}")
    return file_path.resolve(), file_type
