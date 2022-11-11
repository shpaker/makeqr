from enum import Enum, unique
from typing import Tuple

DEFAULT_LINK_SCHEME = "https"
MECARD_SPECIAL_CHARACTERS: str = r'\;,:"'


class AuthType(str, Enum):
    WPA = "wpa"
    WPA2 = "wpa2"
    WEP = "wep"

    @classmethod
    def get_values(
        cls,
    ) -> Tuple[str, ...]:
        return tuple(auth.value for auth in AuthType)


@unique
class WifiMecardParam(str, Enum):
    HIDDEN = "H"
    SSID = "S"
    AUTH = "T"
    PASSWORD = "P"


@unique
class DataScheme(str, Enum):
    WIFI = "WIFI"
    MAILTO = "mailto"
    TEL = "tel"
    SMS = "sms"
    GEO = "geo"
