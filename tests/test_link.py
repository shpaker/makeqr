from makeqr.makers import make_link

LINK = "http://some.url"


def test_make_link() -> None:
    data = make_link(url=LINK)
    assert data == LINK


def test_make_link_simple_with_param() -> None:
    param = {
        "foo": "b a r",
        "baz": "5",
    }
    data = make_link(url=LINK, params=param)
    assert data == f"{LINK}?foo=b%20a%20r&baz=5"


def test_make_link_param_with_param() -> None:
    link = f"{LINK}?test=test"
    param = {"foo": "b a r", "baz": 5}
    data = make_link(url=link, params=param)
    assert data == f"{link}&foo=b%20a%20r&baz=5"
