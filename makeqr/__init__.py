from importlib.metadata import PackageNotFoundError, version

from makeqr.makeqr import MakeQR
from makeqr.models import (
    QRDataModel,
    QRDataModelType,
    QREventModel,
    QRGeoModel,
    QRLinkModel,
    QRMailToModel,
    QRMeCardModel,
    QROtpModel,
    QRSMSModel,
    QRTelModel,
    QRTextModel,
    QRVCardModel,
    QRWiFiModel,
)

try:
    __version__ = version("makeqr")
except PackageNotFoundError:  # pragma: no cover -- running from a source tree
    __version__ = "0.0.0.dev0"

#: Deprecated alias of :data:`__version__`.
VERSION = __version__

__all__ = (
    "VERSION",
    "MakeQR",
    "QRDataModel",
    "QRDataModelType",
    "QREventModel",
    "QRGeoModel",
    "QRLinkModel",
    "QRMailToModel",
    "QRMeCardModel",
    "QROtpModel",
    "QRSMSModel",
    "QRTelModel",
    "QRTextModel",
    "QRVCardModel",
    "QRWiFiModel",
    "__version__",
)
