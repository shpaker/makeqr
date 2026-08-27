import pytest
from pydantic import ValidationError

from makeqr.models import QRGeoModel


def test_make_geo() -> None:
    data = QRGeoModel(latitude=1.5, longitude=2)
    assert data.qr_data == "geo:1.5,2.0"


def test_negative_coordinates() -> None:
    data = QRGeoModel(latitude=-33.86, longitude=151.2)
    assert data.qr_data == "geo:-33.86,151.2"


def test_non_numeric_is_rejected() -> None:
    with pytest.raises(ValidationError):
        QRGeoModel(latitude="north", longitude=1.0)
