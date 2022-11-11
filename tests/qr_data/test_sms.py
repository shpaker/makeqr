from makeqr.models import QRSMSModel


def test_make_tel() -> None:
    data = QRSMSModel(recipients=["recipients1", "recipients2"], body="wow")
    assert data.qr_data == "sms:recipients1,recipients2?body=wow"
