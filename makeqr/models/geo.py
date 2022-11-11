from click import types
from pydantic import Field

from makeqr.constants import DataScheme
from makeqr.qr_data_model import QrDataBaseModel
from makeqr.utils import make_link_data


class QRGeoModel(
    QrDataBaseModel,
):
    latitude: float = Field(
        alias="lat",
        click_option_type=types.FLOAT,
    )
    longitude: float = Field(
        alias="long",
        click_option_type=types.FLOAT,
    )

    @property
    def qr_data(self) -> str:
        return make_link_data(
            schema=DataScheme.GEO,
            link=(
                str(self.latitude),
                str(self.longitude),
            ),
        )
