from makeqr.models.geo import GeoModel


def test_make_geo() -> None:
    data = GeoModel(latitude=1.5, longitude=2)
    assert data.qr_data == "geo:1.5,2.0"