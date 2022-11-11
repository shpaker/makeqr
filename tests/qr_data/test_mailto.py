from makeqr.models import QRMailToModel


def test_make_mailto() -> None:
    data = QRMailToModel(
        to="aaa@aaa.aa",
    )
    assert data.qr_data == "mailto:aaa@aaa.aa"


def test_make_mailto_with_subject() -> None:
    data = QRMailToModel(
        to="aaa@aaa.aa",
        subject="test",
    )
    assert data.qr_data == "mailto:aaa@aaa.aa?subject=test"


def test_make_mailto_with_subject_and_body() -> None:
    data = QRMailToModel(
        to="aaa@aaa.aa",
        subject="test",
        body="foo",
    )
    assert data.qr_data == "mailto:aaa@aaa.aa?subject=test&body=foo"


def test_make_mailto_with_subject_and_cc() -> None:
    data = QRMailToModel(
        to="aaa@aaa.aa",
        subject="test",
        cc=["foo@bar.baz", "baz@bar.baz"],
    )
    assert (
        data.qr_data
        == "mailto:aaa@aaa.aa?subject=test&cc=foo%40bar.baz%2Cbaz%40bar.baz"
    )
