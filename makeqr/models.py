from abc import ABC, abstractmethod
from datetime import UTC, datetime
from enum import StrEnum
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
    VCARD_SPECIAL_CHARACTERS,
    AuthType,
    DataScheme,
    MeCardParam,
    OtpAlgorithm,
    OtpType,
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


class QREventModel(
    QRDataModel,
):
    summary: str = Field(
        alias="s",
        description="Event title",
    )
    start: datetime = Field(
        alias="st",
        description="Start, ISO 8601, e.g. 2026-09-01T12:00",
    )
    end: datetime | None = Field(
        None,
        alias="et",
        description="End, ISO 8601",
    )
    location: str | None = Field(
        None,
        alias="l",
        description="Venue or address",
    )
    description: str | None = Field(
        None,
        alias="d",
        description="Event details",
    )

    @model_validator(mode="after")
    def check_end_after_start(self) -> "QREventModel":
        if self.end is None:
            return self
        if (self.start.tzinfo is None) != (self.end.tzinfo is None):
            msg = "start and end must both be naive or both timezone-aware"
            raise ValueError(msg)
        if self.end <= self.start:
            msg = "end must be after start"
            raise ValueError(msg)
        return self

    @property
    def qr_data(self) -> str:
        lines = [
            "BEGIN:VEVENT",
            f"SUMMARY:{_escape_vcard(self.summary)}",
            f"DTSTART:{_format_vevent_datetime(self.start)}",
        ]
        if self.end is not None:
            lines.append(f"DTEND:{_format_vevent_datetime(self.end)}")
        if self.location:
            lines.append(f"LOCATION:{_escape_vcard(self.location)}")
        if self.description:
            lines.append(f"DESCRIPTION:{_escape_vcard(self.description)}")
        lines.append("END:VEVENT")
        return "\r\n".join(lines)


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


class QRMeCardModel(
    QRDataModel,
):
    last_name: str = Field(
        alias="l",
        description="Last name",
    )
    first_name: str | None = Field(
        None,
        alias="f",
        description="First name",
    )
    tel: str | None = Field(
        None,
        alias="t",
        description="Telephone number",
    )
    email: EmailStr | None = Field(
        None,
        alias="e",
        description="E-mail address",
    )
    url: str | None = Field(
        None,
        alias="u",
        description="Website",
    )
    note: str | None = Field(
        None,
        alias="n",
        description="Free-form note",
    )

    @property
    def qr_data(self) -> str:
        name = _escape_mecard(self.last_name)
        if self.first_name:
            name = f"{name},{_escape_mecard(self.first_name)}"
        fields: dict[StrEnum, str] = {
            MeCardParam.NAME: name,
        }
        if self.tel:
            fields[MeCardParam.TEL] = _escape_mecard(self.tel)
        if self.email:
            fields[MeCardParam.EMAIL] = _escape_mecard(self.email)
        if self.url:
            fields[MeCardParam.URL] = _escape_mecard(self.url)
        if self.note:
            fields[MeCardParam.NOTE] = _escape_mecard(self.note)
        return make_mecard_data(
            title=DataScheme.MECARD.value,
            fields=fields,
        )


class QROtpModel(
    QRDataModel,
):
    type: OtpType = Field(
        OtpType.TOTP,
        alias="t",
        description="One-time password type",
    )
    label: str = Field(
        alias="l",
        description="Account the key belongs to, e.g. alice@example.com",
    )
    secret: SecretStr = Field(
        alias="s",
        description="Base32-encoded shared secret",
    )
    issuer: str | None = Field(
        None,
        alias="i",
        description="Provider or service name",
    )
    algorithm: OtpAlgorithm | None = Field(
        None,
        alias="a",
        description="HMAC hash algorithm",
    )
    digits: int | None = Field(
        None,
        alias="d",
        description="Number of digits in a code",
    )
    period: int | None = Field(
        None,
        alias="p",
        description="Code lifetime in seconds, totp only",
    )
    counter: int | None = Field(
        None,
        alias="c",
        description="Initial counter value, hotp only",
    )

    @model_validator(mode="after")
    def check_type_specific_params(self) -> "QROtpModel":
        if self.type is OtpType.HOTP and self.counter is None:
            msg = "counter is required when type is hotp"
            raise ValueError(msg)
        if self.type is OtpType.TOTP and self.counter is not None:
            msg = "counter is only valid when type is hotp"
            raise ValueError(msg)
        if self.type is OtpType.HOTP and self.period is not None:
            msg = "period is only valid when type is totp"
            raise ValueError(msg)
        return self

    @property
    def qr_data(self) -> str:
        label = self.label if self.issuer is None else f"{self.issuer}:{self.label}"
        args = [f"secret={quote(self.secret.get_secret_value())}"]
        if self.issuer is not None:
            args.append(f"issuer={quote(self.issuer)}")
        if self.algorithm is not None:
            args.append(f"algorithm={self.algorithm.value}")
        # Numeric parameters are compared to None: 0 is a valid HOTP counter.
        if self.digits is not None:
            args.append(f"digits={self.digits}")
        if self.period is not None:
            args.append(f"period={self.period}")
        if self.counter is not None:
            args.append(f"counter={self.counter}")
        return f"{DataScheme.OTPAUTH.value}://{self.type.value}/{quote(label, safe='')}?{'&'.join(args)}"


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


class QRVCardModel(
    QRDataModel,
):
    last_name: str = Field(
        alias="l",
        description="Last name",
    )
    first_name: str | None = Field(
        None,
        alias="f",
        description="First name",
    )
    phones: tuple[str, ...] = Field(
        (),
        alias="t",
        description="Telephone number, repeat for several numbers",
    )
    email: EmailStr | None = Field(
        None,
        alias="e",
        description="E-mail address",
    )
    org: str | None = Field(
        None,
        alias="o",
        description="Organization",
    )
    title: str | None = Field(
        None,
        alias="ti",
        description="Job title",
    )
    url: str | None = Field(
        None,
        alias="u",
        description="Website",
    )

    @property
    def qr_data(self) -> str:
        last = _escape_vcard(self.last_name)
        first = _escape_vcard(self.first_name) if self.first_name else ""
        full_name = f"{first} {last}".strip()
        lines = [
            "BEGIN:VCARD",
            "VERSION:3.0",
            f"N:{last};{first}",
            f"FN:{full_name}",
        ]
        lines.extend(f"TEL:{phone}" for phone in self.phones)
        if self.email:
            lines.append(f"EMAIL:{self.email}")
        if self.org:
            lines.append(f"ORG:{_escape_vcard(self.org)}")
        if self.title:
            lines.append(f"TITLE:{_escape_vcard(self.title)}")
        if self.url:
            lines.append(f"URL:{self.url}")
        lines.append("END:VCARD")
        return "\r\n".join(lines)


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
        fields: dict[StrEnum, str] = {
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


def _escape_vcard(
    value: str,
) -> str:
    for spec_char in VCARD_SPECIAL_CHARACTERS:
        value = value.replace(spec_char, f"\\{spec_char}")
    return value.replace("\r\n", "\\n").replace("\r", "\\n").replace("\n", "\\n")


def _format_vevent_datetime(
    value: datetime,
) -> str:
    # Naive datetimes encode as floating local time; aware ones as UTC.
    if value.tzinfo is None:
        return value.strftime("%Y%m%dT%H%M%S")
    return value.astimezone(UTC).strftime("%Y%m%dT%H%M%SZ")
