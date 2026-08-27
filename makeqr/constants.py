from enum import StrEnum

DEFAULT_LINK_SCHEME = "https"
DEFAULT_IMAGE_FORMAT = "png"
MECARD_SPECIAL_CHARACTERS: str = r'\;,:"'
# vCard/vEvent TEXT values escape fewer characters than MECARD: no ':' or '"'.
# The backslash must stay first so already-added escapes are not escaped again.
VCARD_SPECIAL_CHARACTERS: str = r"\;,"


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


class MeCardParam(StrEnum):
    NAME = "N"
    TEL = "TEL"
    EMAIL = "EMAIL"
    URL = "URL"
    NOTE = "NOTE"


class OtpType(StrEnum):
    TOTP = "totp"
    HOTP = "hotp"


class OtpAlgorithm(StrEnum):
    # The otpauth URI expects the algorithm name in upper case verbatim.
    SHA1 = "SHA1"
    SHA256 = "SHA256"
    SHA512 = "SHA512"


class DataScheme(StrEnum):
    WIFI = "WIFI"
    MECARD = "MECARD"
    MAILTO = "mailto"
    OTPAUTH = "otpauth"
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
