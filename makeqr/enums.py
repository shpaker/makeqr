from enum import Enum, unique


class AuthType(str, Enum):
    WPA = "wpa"
    WPA2 = "wpa2"
    WEP = "wep"


@unique
class ImageType(str, Enum):
    SVG = ".svg"
    PNG = ".png"


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
