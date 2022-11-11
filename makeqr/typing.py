from typing import TypeVar

from makeqr.qr_data_model import QrDataBaseModel

QRDataModel = TypeVar("QRDataModel", bound=QrDataBaseModel)
