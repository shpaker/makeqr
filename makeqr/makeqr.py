from pathlib import Path
from typing import Any, List, Union

from PIL.Image import Image
from qrcode import QRCode

from makeqr.qr_data_model import QrDataBaseModel
from makeqr.typing import QRDataModel


class MakeQR:
    def __init__(
        self,
        data: Union[str, QRDataModel],
    ) -> None:
        if issubclass(data.__class__, QrDataBaseModel):
            data = data.qr_data
        self._qr: QRCode
        self.data = data

    @property
    def data(self) -> QRCode:
        return self._data

    @data.setter
    def data(
        self,
        value: Union[str, QRDataModel],
    ) -> None:
        if issubclass(value.__class__, QrDataBaseModel):
            value = value.qr_data
        self._data = value
        self._qr = QRCode(
            #
        )
        self._qr.add_data(value)

    @property
    def matrix(
        self,
    ) -> List[List[bool]]:
        qr = QRCode()
        qr.add_data(self._data)
        matrix: List[List[bool]] = qr.get_matrix()
        return matrix

    @property
    def pil_image(
        self,
    ) -> Image:
        self._qr.make(fit=True)
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
