from enum import StrEnum

DEFAULT_LINK_SCHEME = "https"
DEFAULT_IMAGE_FORMAT = "png"
MECARD_SPECIAL_CHARACTERS: str = r'\;,:"'


class AuthType(StrEnum):
    WPA = "wpa"
    WPA2 = "wpa2"
    WEP = "wep"

    @classmethod
    def get_values(
        cls,
    ) -> tuple[str, ...]:
        return tuple(auth.value for auth in cls)


class WifiMecardParam(StrEnum):
    HIDDEN = "H"
    SSID = "S"
    AUTH = "T"
    PASSWORD = "P"


class DataScheme(StrEnum):
    WIFI = "WIFI"
    MAILTO = "mailto"
    TEL = "tel"
    SMS = "sms"
    GEO = "geo"


class ErrorCorrectionLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    QUARTILE = "quartile"
    HIGH = "high"

    @classmethod
    def get_values(
        cls,
    ) -> tuple[str, ...]:
        return tuple(level.value for level in cls)
