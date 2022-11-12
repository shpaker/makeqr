from typing import TypeVar

from makeqr.models import _QRDataBaseModel

QRDataModelType = TypeVar(  # pylint: disable=invalid-name
    "QRDataModelType",
    bound=_QRDataBaseModel,
)
