from typing import Any, Dict, List, Optional, Union
from urllib.parse import quote

from .utils import (
    AuthType,
    DataScheme,
    WifiMecardParam,
    make_link_data,
    make_mecard_data,
)

MECARD_SPECIAL_CHARACTERS: str = r'\;,:"'


def make_wifi(
    ssid: str,
    auth: AuthType = AuthType.NOPASS,
    password: Optional[str] = None,
    hidden: bool = False,
) -> str:
    if auth is AuthType.WPA2:
        auth = AuthType.WPA

    if not isinstance(ssid, str):
        ssid = str(ssid)

    if password and not isinstance(password, str):
        password = str(password)

    for spec_char in MECARD_SPECIAL_CHARACTERS:
        ssid = ssid.replace(spec_char, f"\\{spec_char}")
        if password:
            password = password.replace(spec_char, f"\\{spec_char}")

    fields = {
        WifiMecardParam.AUTH: auth.value,
        WifiMecardParam.SSID: ssid,
    }

    if hidden:
        fields[WifiMecardParam.HIDDEN] = "true"

    if auth is not AuthType.NOPASS and password:
        fields[WifiMecardParam.PASSWORD] = password

    wifi_data = make_mecard_data(title=DataScheme.WIFI.value, fields=fields)

    return wifi_data


def make_mailto(
    to: str,
    subject: Optional[str] = None,
    cc: Optional[Union[List[str], str]] = None,
    bcc: Optional[Union[List[str], str]] = None,
    body: Optional[str] = None,
) -> str:
    data = f"{DataScheme.MAILTO.value}:{to}"
    args = list()
    if subject:
        args.append(f"subject={quote(subject)}")
    if cc:
        args.append(f'cc={quote(",".join(cc))}')
    if bcc:
        args.append(f'bcc={quote(",".join(bcc))}')
    if body:
        args.append(f"body={quote(body)}")
    if args:
        data = f'{data}?{"&".join(args)}'
    return data


def make_link(
    url: str,
    params: Optional[Dict[str, Any]] = None,
) -> str:
    return make_link_data(link=url, params=params)


def make_tel(
    tel: str,
) -> str:
    return make_link_data(schema=DataScheme.TEL, link=tel)


def make_sms(
    recipients: Optional[List[str]] = None,
    body: Optional[str] = None,
) -> str:
    body_dict = dict(body=body) if body else dict()
    return make_link_data(
        schema=DataScheme.SMS,
        link=recipients,
        params=body_dict,
    )


def make_geo(
    latitude: float,
    longitude: float,
) -> str:
    coords = [str(latitude), str(longitude)]
    return make_link_data(schema=DataScheme.GEO, link=coords)
