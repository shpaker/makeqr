import pytest
from pydantic import ValidationError

from makeqr.models import QRLinkModel


def test_make_link() -> None:
    data = QRLinkModel(url="http://some.url")
    assert data.qr_data == "http://some.url/"


def test_scheme_is_added_when_missing() -> None:
    data = QRLinkModel(url="some.url")
    assert data.qr_data == "https://some.url/"


def test_existing_scheme_is_kept() -> None:
    data = QRLinkModel(url="ftp://some.url")
    assert data.qr_data.startswith("ftp://")


def test_path_and_query_survive() -> None:
    data = QRLinkModel(url="example.com/a/b?c=d")
    assert data.qr_data == "https://example.com/a/b?c=d"


def test_garbage_is_rejected() -> None:
    with pytest.raises(ValidationError):
        QRLinkModel(url="")
