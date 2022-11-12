from enum import Enum
from io import BytesIO
from pathlib import Path
from typing import Any, List, Union

from PIL.Image import Image
from qrcode import (
    ERROR_CORRECT_H,
    ERROR_CORRECT_L,
    ERROR_CORRECT_M,
    ERROR_CORRECT_Q,
    QRCode,
)

from makeqr.constants import DEFAULT_IMAGE_FORMAT, ErrorCorrectionLevel
from makeqr.models import _QRDataBaseModel
from makeqr.typing import QRDataModelType


class _ErrorCorrectionLevelMapping(Enum):
    LOW = ERROR_CORRECT_L
    MEDIUM = ERROR_CORRECT_M
    QUARTILE = ERROR_CORRECT_Q
    HIGH = ERROR_CORRECT_H


class MakeQR:
    def __init__(
        self,
        data: Union[str, QRDataModelType],
        *,
        box_size: int = 10,
        border: int = 1,
        error_correction: ErrorCorrectionLevel = ErrorCorrectionLevel.MEDIUM,
    ) -> None:
        if issubclass(data.__class__, _QRDataBaseModel):
            data = data.qr_data
        self._qr: QRCode
        self._box_size = box_size
        self._border = border
        self._error_correction = error_correction
        self.data = data

    @property
    def data(self) -> QRCode:
        return self._data

    @data.setter
    def data(
        self,
        value: Union[str, QRDataModelType],
    ) -> None:
        if issubclass(value.__class__, _QRDataBaseModel):
            value = value.qr_data
        self._data = value
        _level = _ErrorCorrectionLevelMapping[self._error_correction.name]
        self._qr = QRCode(
            box_size=self._box_size,
            border=self._border,
            error_correction=_level.value,
        )
        self._qr.add_data(value)
        self._qr.make(fit=True)

    @property
    def matrix(
        self,
    ) -> List[List[bool]]:
        matrix: List[List[bool]] = self._qr.get_matrix()
        return matrix

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

    @property
    def pil_image(
        self,
    ) -> Image:
        qr_image = self._qr.make_image()
        return qr_image.get_image()

    def save(
        self,
        path: Union[str, Path],
        **params: Any,
    ) -> None:
        with open(path, "wb") as stream:
            self.pil_image.save(
                stream,
                **params,
            )
