from makeqr.models.sms import SmsModel


def test_make_tel() -> None:
    data = SmsModel(recipients=["recipients1", "recipients2"], body="wow")
    assert data.encode == "sms:recipients1,recipients2?body=wow"
