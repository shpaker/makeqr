from abc import ABC, abstractmethod
from typing import TypeVar
from urllib.parse import quote

from pydantic import (
    AnyUrl,
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    SecretStr,
    field_validator,
    model_validator,
)

from makeqr.constants import (
    DEFAULT_LINK_SCHEME,
    MECARD_SPECIAL_CHARACTERS,
    AuthType,
    DataScheme,
    WifiMecardParam,
)
from makeqr.utils import make_link_data, make_mecard_data


class QRDataModel(
    ABC,
    BaseModel,
):
    """Base class for every payload a QR code can carry.

    Subclasses describe their fields with pydantic and turn themselves into a
    payload string via :attr:`qr_data`, which must be free of side effects.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )

    @property
    @abstractmethod
    def qr_data(self) -> str:
        raise NotImplementedError


QRDataModelType = TypeVar(
    "QRDataModelType",
    bound=QRDataModel,
)


class QRGeoModel(
    QRDataModel,
):
    latitude: float = Field(
        alias="lat",
        description="Latitude in decimal degrees",
    )
    longitude: float = Field(
        alias="long",
        description="Longitude in decimal degrees",
    )

    @property
    def qr_data(self) -> str:
        return make_link_data(
            scheme=DataScheme.GEO,
            link=(
                str(self.latitude),
                str(self.longitude),
            ),
        )


class QRLinkModel(
    QRDataModel,
):
    url: AnyUrl = Field(
        alias="u",
        description="URL, with or without a scheme",
    )

    @field_validator("url", mode="before")
    @classmethod
    def add_default_scheme(
        cls,
        value: str,
    ) -> str:
        if isinstance(value, str) and "://" not in value:
            return f"{DEFAULT_LINK_SCHEME}://{value}"
        return value

    @property
    def qr_data(self) -> str:
        return make_link_data(
            link=str(self.url),
        )


class QRMailToModel(
    QRDataModel,
):
    to: EmailStr = Field(
        alias="t",
        description="Recipient",
    )
    subject: str | None = Field(
        None,
        alias="s",
        description="E-mail subject",
    )
    cc: tuple[EmailStr, ...] = Field(
        (),
        description="Carbon copy, repeat for several addresses",
    )
    bcc: tuple[EmailStr, ...] = Field(
        (),
        description="Blind carbon copy, repeat for several addresses",
    )
    body: str | None = Field(
        None,
        alias="b",
        description="E-mail body",
    )

    @property
    def qr_data(self) -> str:
        data = f"{DataScheme.MAILTO.value}:{self.to}"
        args = []
        if self.subject:
            args.append(f"subject={quote(self.subject)}")
        if self.cc:
            args.append(f"cc={quote(','.join(self.cc))}")
        if self.bcc:
            args.append(f"bcc={quote(','.join(self.bcc))}")
        if self.body:
            args.append(f"body={quote(self.body)}")
        return data if not args else f"{data}?{'&'.join(args)}"


class QRSMSModel(
    QRDataModel,
):
    recipients: tuple[str, ...] = Field(
        alias="r",
        description="Recipient number, repeat for several recipients",
    )
    body: str | None = Field(
        None,
        alias="b",
        description="Message text",
    )

    @property
    def qr_data(self) -> str:
        body_dict = {"body": self.body} if self.body else {}
        return make_link_data(
            scheme=DataScheme.SMS,
            link=self.recipients,
            params=body_dict,
        )


class QRTelModel(
    QRDataModel,
):
    tel: str = Field(
        alias="t",
        description="Telephone number",
    )

    @property
    def qr_data(self) -> str:
        return make_link_data(
            scheme=DataScheme.TEL,
            link=self.tel,
        )


class QRTextModel(
    QRDataModel,
):
    text: str = Field(
        alias="t",
        description="Arbitrary text to encode",
    )

    @property
    def qr_data(self) -> str:
        return self.text


class QRWiFiModel(
    QRDataModel,
):
    ssid: str = Field(
        alias="id",
        description="Network SSID",
    )
    security: AuthType | None = Field(
        None,
        alias="s",
        description="Authentication type",
    )
    password: SecretStr | None = Field(
        None,
        alias="p",
        description="Network password",
    )
    hidden: bool = Field(
        False,
        alias="h",
        description="Set if the SSID is hidden",
    )

    @model_validator(mode="after")
    def check_security_and_password(self) -> "QRWiFiModel":
        if self.security is not None and self.password is None:
            msg = "password is required when security is set"
            raise ValueError(msg)
        return self

    @property
    def qr_data(self) -> str:
        fields = {
            WifiMecardParam.SSID: _escape_mecard(self.ssid),
        }
        if self.hidden:
            fields[WifiMecardParam.HIDDEN] = "true"
        if self.password is not None:
            # WPA2 networks are advertised as WPA: the MECARD format has no
            # separate token for them and readers expect "WPA".
            security = AuthType.WPA if self.security in (None, AuthType.WPA2) else self.security
            fields[WifiMecardParam.PASSWORD] = _escape_mecard(self.password.get_secret_value())
            fields[WifiMecardParam.AUTH] = security.name
        else:
            fields[WifiMecardParam.AUTH] = "nopass"
        return make_mecard_data(
            title=DataScheme.WIFI.value,
            fields=fields,
        )


def _escape_mecard(
    value: str,
) -> str:
    for spec_char in MECARD_SPECIAL_CHARACTERS:
        value = value.replace(spec_char, f"\\{spec_char}")
    return value
