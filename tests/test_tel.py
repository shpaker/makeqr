from makeqr.makers import make_tel

TEL = "+79876543210"


def test_make_tel() -> None:
    data = make_tel(tel=TEL)
    assert data == f"tel:{TEL}"
