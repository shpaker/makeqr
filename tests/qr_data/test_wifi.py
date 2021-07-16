from makeqr.enums import AuthType
from makeqr.models.wifi import WiFiModel


def test_make_wifi() -> None:
    data = WiFiModel(ssid="test")
    assert data.qr_data == "WIFI:S:test;;"


def test_make_wifi_with_wpa_without_password() -> None:
    data = WiFiModel(ssid="test", security=AuthType.WPA2)
    assert data.qr_data == "WIFI:S:test;;"


def test_make_wifi_without_wpa_with_password() -> None:
    data = WiFiModel(ssid="test", password=AuthType.WPA2)
    assert data.qr_data == "WIFI:S:test;;"


def test_make_wifi_with_wpa_with_password() -> None:
    data = WiFiModel(ssid="test", security=AuthType.WPA2, password="secret")
    assert data.qr_data == "WIFI:S:test;P:secret;T:wpa;;"


def test_make_wifi_hidden() -> None:
    data = WiFiModel(ssid="test", hidden=True)
    assert data.qr_data == "WIFI:S:test;H:true;;"