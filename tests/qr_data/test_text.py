from makeqr.models import QRTextModel


def test_make_text() -> None:
    assert QRTextModel(text="hello world").qr_data == "hello world"


def test_text_is_passed_through_verbatim() -> None:
    raw = 'WIFI:S:not;really"escaped'
    assert QRTextModel(text=raw).qr_data == raw
