from abc import ABC, abstractmethod
from typing import Optional, Tuple
from urllib.parse import quote

from click import types
from pydantic import AnyUrl, BaseModel, EmailStr, Extra, Field, validator

from makeqr.constants import (
    DEFAULT_LINK_SCHEME,
    MECARD_SPECIAL_CHARACTERS,
    AuthType,
    DataScheme,
    WifiMecardParam,
)
from makeqr.utils import make_link_data, make_mecard_data


class _QRDataBaseModel(
    ABC,
    BaseModel,
    extra=Extra.forbid,
    allow_population_by_field_name=True,
):
    @property
    @abstractmethod
    def qr_data(self) -> str:
        raise NotImplementedError


class QRGeoModel(
    _QRDataBaseModel,
):
    latitude: float = Field(
        alias="lat",
        click_option_type=types.FLOAT,
    )
    longitude: float = Field(
        alias="long",
        click_option_type=types.FLOAT,
    )

    @property
    def qr_data(self) -> str:
        return make_link_data(
            schema=DataScheme.GEO,
            link=(
                str(self.latitude),
                str(self.longitude),
            ),
        )


class QRLinkModel(
    _QRDataBaseModel,
):
    url: AnyUrl = Field(
        alias="u",
        description="URL",
        click_type=types.STRING,
    )

    @property
    def qr_data(self) -> str:
        return make_link_data(
            link=self.url,
        )

    @classmethod
    @validator("url", pre=True)
    def url_validator(
        cls,
        value: str,
    ) -> str:
        if "://" not in value:
            return f"{DEFAULT_LINK_SCHEME}://{value}"
        return value


class QRMailToModel(
    _QRDataBaseModel,
):
    to: EmailStr = Field(
        description="Recipient",
        alias="t",
    )
    subject: Optional[str] = Field(
        None,
        alias="s",
    )
    cc: Tuple[EmailStr, ...] = Field(
        (),
        description="Carbon copy",
        click_option_multiple=True,
    )
    bcc: Tuple[EmailStr, ...] = Field(
        (),
        description="Blind carbon copy",
        click_option_multiple=True,
    )
    body: Optional[str] = Field(
        None,
        description="E-mail body",
        alias="b",
    )

    @property
    def qr_data(self) -> str:
        data = f"{DataScheme.MAILTO.value}:{self.to}"
        args = []
        if self.subject:
            args.append(f"subject={quote(self.subject)}")
        if self.cc:
            args.append(f'cc={quote(",".join(self.cc))}')
        if self.bcc:
            args.append(f'bcc={quote(",".join(self.bcc))}')
        if self.body:
            args.append(f"body={quote(self.body)}")
        return data if not args else f'{data}?{"&".join(args)}'


class QRSMSModel(
    _QRDataBaseModel,
):
    recipients: Tuple[str, ...] = Field(
        [],
        alias="r",
        click_option_multiple=True,
    )
    body: Optional[str] = Field(
        None,
        alias="b",
    )

    @property
    def qr_data(self) -> str:
        body_dict = {"body": self.body} if self.body else {}
        return make_link_data(
            schema=DataScheme.SMS,
            link=self.recipients,
            params=body_dict,
        )


class QRTelModel(
    _QRDataBaseModel,
):
    tel: str = Field(
        False,
        description="Telephone number",
        alias="t",
    )

    @property
    def qr_data(self) -> str:
        return make_link_data(
            schema=DataScheme.TEL,
            link=self.tel,
        )


class QRTextModel(
    _QRDataBaseModel,
):
    text: str = Field(
        alias="t",
    )

    @property
    def qr_data(self) -> str:
        return self.text


class QRWiFiModel(
    _QRDataBaseModel,
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
            fields[WifiMecardParam.AUTH] = self.security.value
        return make_mecard_data(
            title=DataScheme.WIFI.value,
            fields=fields,
        )
