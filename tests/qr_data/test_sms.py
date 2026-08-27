from makeqr.models import QRSMSModel


def test_make_sms() -> None:
    data = QRSMSModel(recipients=["recipients1", "recipients2"], body="wow")
    assert data.qr_data == "sms:recipients1,recipients2?body=wow"


def test_sms_without_body() -> None:
    data = QRSMSModel(recipients=["+123"])
    assert data.qr_data == "sms:+123"


def test_body_is_percent_encoded() -> None:
    data = QRSMSModel(recipients=["+123"], body="hi there & bye")
    assert data.qr_data == "sms:+123?body=hi%20there%20%26%20bye"
