from makeqr.makers import make_geo


def test_make_geo() -> None:
    geo = (1, 2)
    data = make_geo(*geo)
    assert data == f"geo:{geo[0]},{geo[1]}"
