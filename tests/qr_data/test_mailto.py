from makeqr.models.mailto import MailToModel


def test_make_mailto() -> None:
    data = MailToModel(
        to="aaa@aaa.aa",
    )
    assert data.encode == "mailto:aaa@aaa.aa"


def test_make_mailto_with_subject() -> None:
    data = MailToModel(
        to="aaa@aaa.aa",
        subject="test",
    )
    assert data.encode == "mailto:aaa@aaa.aa?subject=test"


def test_make_mailto_with_subject_and_body() -> None:
    data = MailToModel(
        to="aaa@aaa.aa",
        subject="test",
        body="foo",
    )
    assert data.encode == "mailto:aaa@aaa.aa?subject=test&body=foo"


def test_make_mailto_with_subject_and_cc() -> None:
    data = MailToModel(
        to="aaa@aaa.aa",
        subject="test",
        cc=["foo@bar.baz", "baz@bar.baz"],
    )
    assert (
        data.encode
        == "mailto:aaa@aaa.aa?subject=test&cc=foo%40bar.baz%2Cbaz%40bar.baz"
    )
