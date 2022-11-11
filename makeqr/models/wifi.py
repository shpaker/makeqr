from typing import Optional

from click import types
from pydantic import Field

from makeqr.constants import AuthType, DataScheme, WifiMecardParam
from makeqr.qr_data_model import QrDataBaseModel
from makeqr.utils import make_mecard_data

MECARD_SPECIAL_CHARACTERS: str = r'\;,:"'


class QRWiFiModel(
    QrDataBaseModel,
):
    ssid: str = Field(
        description="Network SSID",
        alias="id",
    )
    security: Optional[AuthType] = Field(
        None,
        description="Authentication type",
        alias="s",
        click_option_type=types.Choice(
            AuthType.get_values(),
            case_sensitive=False,
        ),
    )
    password: Optional[str] = Field(
        None,
        alias="p",
    )
    hidden: bool = Field(
        False,
        description="True if the SSID is hidden",
        alias="h",
        click_option_type=types.BOOL,
    )

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
