from typing import Any, Dict, Optional, Tuple, Union
from urllib.parse import quote

from makeqr.constants import DataScheme, WifiMecardParam


def make_mecard_data(
    title: str,
    fields: Dict[WifiMecardParam, str],
) -> str:
    fields_list = []
    for field, value in fields.items():
        fields_list.append(f"{field.value}:{value}")
    mecard_data = f'{title}:{";".join(fields_list)};;'
    return mecard_data


def make_link_data(
    schema: Optional[DataScheme] = None,
    link: Optional[Union[Tuple[str, ...], str]] = None,
    params: Optional[Dict[str, Any]] = None,
) -> str:
    if isinstance(link, str):
        link = (link,)
    if not link:
        link = ()
    link_str = ",".join(link)
    data = link_str
    if schema:
        data = f"{schema.value}:{data}"
    if params:
        params = {str(param): quote(str(params[param])) for param in params}
        concatenation_char = "&" if "?" in link_str else "?"
        params_list = [f"{param}={value}" for param, value in params.items()]
        params_string = "&".join(params_list)
        data = f"{data}{concatenation_char}{params_string}"
    return data
