from wifi_qrcode import make_geo

GEO = (1, 2)


def test_make_geo():
    data = make_geo(*GEO)
    assert data == f'geo:{GEO[0]},{GEO[1]}'
