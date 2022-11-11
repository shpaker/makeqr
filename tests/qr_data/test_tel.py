from makeqr.models.tel import QRTelModel


def test_make_tel() -> None:
    tel = "+79876543210"
    data = QRTelModel(tel=tel)
    assert data.qr_data == f"tel:{tel}"
