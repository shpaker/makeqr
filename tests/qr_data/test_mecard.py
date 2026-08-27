import pytest
from pydantic import ValidationError

from makeqr.models import QRMeCardModel


def test_minimal_mecard() -> None:
    assert QRMeCardModel(last_name="Doe").qr_data == "MECARD:N:Doe;;"


def test_mecard_with_first_name() -> None:
    data = QRMeCardModel(last_name="Doe", first_name="John")
    assert data.qr_data == "MECARD:N:Doe,John;;"


def test_full_mecard() -> None:
    data = QRMeCardModel(
        last_name="Doe",
        first_name="John",
        tel="+79876543210",
        email="john@doe.com",
        url="https://doe.com",
        note="Friend",
    )
    assert data.qr_data == r"MECARD:N:Doe,John;TEL:+79876543210;EMAIL:john@doe.com;URL:https\://doe.com;NOTE:Friend;;"


def test_name_parts_are_escaped() -> None:
    data = QRMeCardModel(last_name="Do;e", first_name="Jo,hn")
    assert data.qr_data == r"MECARD:N:Do\;e,Jo\,hn;;"


def test_invalid_email_is_rejected() -> None:
    with pytest.raises(ValidationError):
        QRMeCardModel(last_name="Doe", email="nope")


def test_qr_data_is_idempotent_and_leaves_the_model_alone() -> None:
    data = QRMeCardModel(last_name="Do;e")
    first = data.qr_data
    assert data.qr_data == first
    assert data.last_name == "Do;e"
