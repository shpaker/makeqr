import pytest
from pydantic import ValidationError

from makeqr.models import QRVCardModel


def test_minimal_vcard() -> None:
    data = QRVCardModel(last_name="Doe")
    assert data.qr_data == "BEGIN:VCARD\r\nVERSION:3.0\r\nN:Doe;\r\nFN:Doe\r\nEND:VCARD"


def test_full_vcard() -> None:
    data = QRVCardModel(
        last_name="Doe",
        first_name="John",
        phones=("+79876543210", "+79876543211"),
        email="john@doe.com",
        org="ACME",
        title="Engineer",
        url="https://doe.com",
    )
    assert data.qr_data == (
        "BEGIN:VCARD\r\n"
        "VERSION:3.0\r\n"
        "N:Doe;John\r\n"
        "FN:John Doe\r\n"
        "TEL:+79876543210\r\n"
        "TEL:+79876543211\r\n"
        "EMAIL:john@doe.com\r\n"
        "ORG:ACME\r\n"
        "TITLE:Engineer\r\n"
        "URL:https://doe.com\r\n"
        "END:VCARD"
    )


def test_special_characters_are_escaped() -> None:
    data = QRVCardModel(last_name="Doe;Jr", org=r"A,B\C")
    assert r"N:Doe\;Jr;" in data.qr_data
    assert r"ORG:A\,B\\C" in data.qr_data


def test_newlines_become_literal_n() -> None:
    data = QRVCardModel(last_name="Doe", title="Line1\nLine2")
    assert r"TITLE:Line1\nLine2" in data.qr_data


def test_invalid_email_is_rejected() -> None:
    with pytest.raises(ValidationError):
        QRVCardModel(last_name="Doe", email="nope")


def test_qr_data_is_idempotent_and_leaves_the_model_alone() -> None:
    data = QRVCardModel(last_name="Doe;Jr", first_name="John")
    first = data.qr_data
    assert data.qr_data == first
    assert data.last_name == "Doe;Jr"
    assert data.first_name == "John"
