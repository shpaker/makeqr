from makeqr.models.tel import TelModel


def test_make_tel() -> None:
    tel = "+79876543210"
    data = TelModel(tel=tel)
    assert data.encode == f"tel:{tel}"
