from pathlib import Path
from typing import List, Optional, TypeVar, Union

from PIL.Image import Image
from qrcode import QRCode

from makeqr.base import QrDataBaseModel

T = TypeVar("T", bound=QrDataBaseModel)


class MakeQR:
    def __init__(
        self,
        data: Union[str, T],
    ) -> None:
        if issubclass(data.__class__, QrDataBaseModel):
            data = data.qr_data
        self._qr: Optional[QRCode] = None
        self.data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value
        self._qr = QRCode(
            # todo: config
        )
        self._qr.add_data(value)

    @property
    def matrix(
        self,
    ) -> List[List[bool]]:
        qr = QRCode()
        qr.add_data(self._data)
        return qr.get_matrix()

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
        format=None,  # noqa
        **params,
    ) -> None:
        with open(path, "wb") as stream:
            self.pil_image.save(
                stream,
                format=format,
                **params,
            )
