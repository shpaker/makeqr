import os
from enum import Enum
from io import BytesIO
from pathlib import Path
from typing import Any

from PIL import Image
from PIL.Image import Image as PILImage
from qrcode.constants import (
    ERROR_CORRECT_H,
    ERROR_CORRECT_L,
    ERROR_CORRECT_M,
    ERROR_CORRECT_Q,
)
from qrcode.main import QRCode

from makeqr.constants import DEFAULT_IMAGE_FORMAT, ErrorCorrectionLevel
from makeqr.models import QRDataModel


class _ErrorCorrectionLevelMapping(Enum):
    LOW = ERROR_CORRECT_L
    MEDIUM = ERROR_CORRECT_M
    QUARTILE = ERROR_CORRECT_Q
    HIGH = ERROR_CORRECT_H


def resolve_image_format(
    path: str | Path,
) -> str:
    """Return the PIL format for ``path``, or raise ``ValueError``.

    Resolved up front so that a bad extension never reaches the filesystem.
    """
    suffix = Path(path).suffix.lower()
    if not suffix:
        msg = f"no file extension to derive an image format from: {path}"
        raise ValueError(msg)
    extensions = Image.registered_extensions()
    if suffix not in extensions:
        msg = f"unknown file extension: {suffix}"
        raise ValueError(msg)
    return extensions[suffix]


class MakeQR:
    def __init__(
        self,
        data: str | QRDataModel,
        *,
        box_size: int = 10,
        border: int = 1,
        error_correction: ErrorCorrectionLevel | str = ErrorCorrectionLevel.MEDIUM,
    ) -> None:
        self._box_size = box_size
        self._border = border
        self._error_correction = ErrorCorrectionLevel(error_correction)
        self.data = data

    @property
    def data(self) -> str:
        return self._data

    @data.setter
    def data(
        self,
        value: str | QRDataModel,
    ) -> None:
        self._data = value.qr_data if isinstance(value, QRDataModel) else value
        level = _ErrorCorrectionLevelMapping[self._error_correction.name]
        self._qr = QRCode(
            box_size=self._box_size,
            border=self._border,
            error_correction=level.value,
        )
        self._qr.add_data(self._data)
        self._qr.make(fit=True)

    @property
    def matrix(
        self,
    ) -> list[list[bool]]:
        matrix: list[list[bool]] = self._qr.get_matrix()
        return matrix

    @property
    def pil_image(
        self,
    ) -> PILImage:
        image: PILImage = self._qr.make_image().get_image()
        return image

    def make_image_data(
        self,
        image_format: str = DEFAULT_IMAGE_FORMAT,
        **params: Any,
    ) -> bytes:
        buffer = BytesIO()
        self.pil_image.save(
            buffer,
            format=image_format,
            **params,
        )
        return buffer.getvalue()

    def save(
        self,
        path: str | Path,
        **params: Any,
    ) -> None:
        """Write the QR code to ``path``.

        The image is rendered in memory and written to a temporary file next to
        the target, then moved into place. A failure — an unusable extension,
        an encoding error — leaves any existing file at ``path`` untouched.
        """
        path = Path(path)
        image_format = resolve_image_format(path)
        payload = self.make_image_data(image_format, **params)

        tmp_path = path.with_name(f".{path.name}.{os.getpid()}.tmp")
        try:
            tmp_path.write_bytes(payload)
            os.replace(tmp_path, path)  # noqa: PTH105 -- Path has no atomic replace
        except BaseException:
            tmp_path.unlink(missing_ok=True)
            raise
