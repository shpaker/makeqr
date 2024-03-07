from makeqr.models import QRLinkModel

LINK = "http://some.url"


def test_make_link() -> None:
    data = QRLinkModel(url=LINK)
    assert data.qr_data == f"{LINK}/"
