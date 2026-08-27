import pytest
from pydantic import ValidationError

from makeqr.constants import AuthType
from makeqr.models import QRWiFiModel


def test_make_wifi() -> None:
    data = QRWiFiModel(ssid="test")
    assert data.qr_data == "WIFI:S:test;T:nopass;;"


def test_make_wifi_hidden() -> None:
    data = QRWiFiModel(ssid="test", hidden=True)
    assert data.qr_data == "WIFI:S:test;H:true;T:nopass;;"


def test_make_wifi_with_wpa_with_password() -> None:
    data = QRWiFiModel(ssid="test", security=AuthType.WPA2, password="secret")
    assert data.qr_data == "WIFI:S:test;P:secret;T:WPA;;"


def test_make_wifi_wep() -> None:
    data = QRWiFiModel(ssid="test", security=AuthType.WEP, password="secret")
    assert data.qr_data == "WIFI:S:test;P:secret;T:WEP;;"


def test_password_without_security_defaults_to_wpa() -> None:
    data = QRWiFiModel(ssid="test", password="secret")
    assert data.qr_data == "WIFI:S:test;P:secret;T:WPA;;"


def test_security_without_password_is_rejected() -> None:
    with pytest.raises(ValidationError, match="password is required"):
        QRWiFiModel(ssid="test", security=AuthType.WPA)


def test_special_characters_are_escaped_once() -> None:
    data = QRWiFiModel(ssid="my;ssid", security=AuthType.WPA, password=r'p\w:x,y"z')
    assert data.qr_data == r"WIFI:S:my\;ssid;P:p\\w\:x\,y\"z;T:WPA;;"


def test_qr_data_is_idempotent_and_leaves_the_model_alone() -> None:
    data = QRWiFiModel(ssid="my;ssid", security=AuthType.WPA2, password="p;w")
    first = data.qr_data
    assert data.qr_data == first
    assert data.qr_data == first
    assert data.ssid == "my;ssid"
    assert data.security is AuthType.WPA2
    assert data.password is not None
    assert data.password.get_secret_value() == "p;w"


def test_password_is_masked_in_dumps() -> None:
    data = QRWiFiModel(ssid="test", password="TopSecret")
    assert "TopSecret" not in data.model_dump_json()
