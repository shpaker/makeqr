from pydantic import Field

from makeqr.base import QrDataBaseModel
from makeqr.enums import DataScheme
from makeqr.utils import make_link_data


class GeoModel(
    QrDataBaseModel,
):
    latitude: float
    longitude: float

    @property
    def qr_data(self) -> str:
        return make_link_data(
            schema=DataScheme.GEO,
            link=[
                str(self.latitude),
                str(self.longitude),
            ],
        )
