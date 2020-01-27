from wifi_qrcode import make_tel

TEL = '+79876543210'


def test_make_tel():
    data = make_tel(tel=TEL)
    assert data == f'tel:{TEL}'
