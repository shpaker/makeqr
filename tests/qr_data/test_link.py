from makeqr.models import QRLinkModel

LINK = "http://some.url"


def test_ccc() -> None:
    data = QRLinkModel(url=LINK)
    assert data.qr_data == f"{LINK}?foo=b%20a%20r", data.qr_data


def test_make_link() -> None:
    data = QRLinkModel(url=LINK)
    assert data.qr_data == LINK


def test_make_link_simple_with_param() -> None:
    param = {
        "foo": "b a r",
        "baz": "5",
    }
    data = QRLinkModel(url=LINK, params=param)
    assert data.qr_data == f"{LINK}?foo=b%20a%20r&baz=5"


def test_make_link_param_with_param() -> None:
    link = f"{LINK}?test=test"
    param = {"foo": "b a r", "baz": 5}
    data = QRLinkModel(url=link, params=param)
    assert data.qr_data == f"{link}&foo=b%20a%20r&baz=5"
