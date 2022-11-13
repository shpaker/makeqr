from makeqr.makeqr import MakeQR
from makeqr.models import (
    QRGeoModel,
    QRLinkModel,
    QRMailToModel,
    QRSMSModel,
    QRTelModel,
    QRTextModel,
    QRWiFiModel,
)
from makeqr.typing import QRDataModelType
from makeqr.version import VERSION

__version__ = VERSION
__all__ = (
    "MakeQR",
    "QRDataModelType",
    "QRGeoModel",
    "QRLinkModel",
    "QRMailToModel",
    "QRSMSModel",
    "QRTelModel",
    "QRTextModel",
    "QRWiFiModel",
    "VERSION",
)
