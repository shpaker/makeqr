from typing import Optional

from pydantic import Field

from makeqr.enums import AuthType, DataScheme, WifiMecardParam
from makeqr.models.base import QrDataBaseModel
from makeqr.utils import make_mecard_data

MECARD_SPECIAL_CHARACTERS: str = r'\;,:"'


class WiFiModel(QrDataBaseModel):
    ssid: str = Field(..., min_length=1)
    security: Optional[AuthType] = None
    password: Optional[str] = Field(None, min_length=1)
    hidden: bool = False

    @property
    def qr_data(self) -> str:
        if self.security is AuthType.WPA2:
            self.security = AuthType.WPA
        for spec_char in MECARD_SPECIAL_CHARACTERS:
            self.ssid = self.ssid.replace(spec_char, f"\\{spec_char}")
            if self.password:
                self.password = self.password.replace(
                    spec_char, f"\\{spec_char}"
                )
        fields = {
            WifiMecardParam.SSID: self.ssid,
        }
        if self.hidden:
            fields[WifiMecardParam.HIDDEN] = "true"
        if self.security and self.password:
            fields[WifiMecardParam.PASSWORD] = self.password
            fields[WifiMecardParam.AUTH] = self.security
        return make_mecard_data(
            title=DataScheme.WIFI,
            fields=fields,
        )
