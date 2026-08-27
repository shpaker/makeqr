from collections.abc import Mapping
from enum import StrEnum
from typing import Any
from urllib.parse import quote

from makeqr.constants import DataScheme


def make_mecard_data(
    title: str,
    fields: Mapping[StrEnum, str],
) -> str:
    fields_list = [f"{field.value}:{value}" for field, value in fields.items()]
    return f"{title}:{';'.join(fields_list)};;"


def make_link_data(
    scheme: DataScheme | None = None,
    link: tuple[str, ...] | str | None = None,
    params: dict[str, Any] | None = None,
) -> str:
    if isinstance(link, str):
        link = (link,)
    if not link:
        link = ()
    link_str = ",".join(link)
    data = link_str
    if scheme:
        data = f"{scheme.value}:{data}"
    if params:
        concatenation_char = "&" if "?" in link_str else "?"
        params_list = [f"{param}={quote(str(value))}" for param, value in params.items()]
        data = f"{data}{concatenation_char}{'&'.join(params_list)}"
    return data
