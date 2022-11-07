from enum import Enum

from qrcode import ERROR_CORRECT_H

DEFAULT_OUTPUT: str = "qrcode.png"


class DefaultQRColors(str, Enum):
    FILL = "black"
    BACK = "white"


DEFAULT_QR_IMAGE_PARAMS = {
    "error_correction": ERROR_CORRECT_H,
}
