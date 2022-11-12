from enum import Enum
from typing import Tuple

DEFAULT_LINK_SCHEME = "https"
DEFAULT_IMAGE_FORMAT = "png"
MECARD_SPECIAL_CHARACTERS: str = r'\;,:"'


class AuthType(str, Enum):
    WPA = "wpa"
    WPA2 = "wpa2"
    WEP = "wep"

    @classmethod
    def get_values(
        cls,
    ) -> Tuple[str, ...]:
        return tuple(auth.value for auth in cls)


class WifiMecardParam(str, Enum):
    HIDDEN = "H"
    SSID = "S"
    AUTH = "T"
    PASSWORD = "P"


class DataScheme(str, Enum):
    WIFI = "WIFI"
    MAILTO = "mailto"
    TEL = "tel"
    SMS = "sms"
    GEO = "geo"


class ErrorCorrectionLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    QUARTILE = "quartile"
    HIGH = "high"

    @classmethod
    def get_values(
        cls,
    ) -> Tuple[str, ...]:
        return tuple(auth.value for auth in cls)
