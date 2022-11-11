from pathlib import Path
from typing import Any, List, Union

from PIL.Image import Image
from qrcode import QRCode, constants

from makeqr.models import QRDataBaseModel
from makeqr.typing import QRDataModel


class MakeQR:
    def __init__(
        self,
        data: Union[str, QRDataModel],
        *,
        box_size: int = 10,
        border: int = 4,
        error_correction: int = constants.ERROR_CORRECT_H,
    ) -> None:
        if issubclass(data.__class__, QRDataBaseModel):
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
        value: Union[str, QRDataModel],
    ) -> None:
        if issubclass(value.__class__, QRDataBaseModel):
            value = value.qr_data
        self._data = value
        self._qr = QRCode(
            box_size=self._box_size,
            border=self._border,
            error_correction=self._error_correction,
        )
        self._qr.add_data(value)
        self._qr.make(fit=True)

    @property
    def matrix(
        self,
    ) -> List[List[bool]]:
        matrix: List[List[bool]] = self._qr.get_matrix()
        return matrix

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
