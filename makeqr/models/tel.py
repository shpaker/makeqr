from pydantic import Field

from makeqr.constants import DataScheme
from makeqr.qr_data_model import QrDataBaseModel
from makeqr.utils import make_link_data


class QRTelModel(
    QrDataBaseModel,
):
    tel: str = Field(
        False,
        description="Telephone number",
        alias="t",
    )

    @property
    def qr_data(self) -> str:
        return make_link_data(
            schema=DataScheme.TEL,
            link=self.tel,
        )
