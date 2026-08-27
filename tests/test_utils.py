from makeqr.constants import DataScheme, WifiMecardParam
from makeqr.utils import make_link_data, make_mecard_data


def test_make_link_data_without_anything() -> None:
    assert make_link_data() == ""


def test_make_link_data_string_link() -> None:
    assert make_link_data(scheme=DataScheme.TEL, link="+123") == "tel:+123"


def test_make_link_data_joins_multiple_links() -> None:
    assert make_link_data(scheme=DataScheme.SMS, link=("a", "b")) == "sms:a,b"


def test_make_link_data_appends_params() -> None:
    result = make_link_data(scheme=DataScheme.SMS, link="a", params={"body": "x y"})
    assert result == "sms:a?body=x%20y"


def test_make_link_data_uses_ampersand_when_query_present() -> None:
    result = make_link_data(link="http://x/?a=1", params={"b": "2"})
    assert result == "http://x/?a=1&b=2"


def test_make_mecard_data() -> None:
    fields = {WifiMecardParam.SSID: "net", WifiMecardParam.PASSWORD: "pw"}
    assert make_mecard_data(title="WIFI", fields=fields) == "WIFI:S:net;P:pw;;"
