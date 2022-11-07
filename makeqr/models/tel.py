from makeqr.base import QrDataBaseModel
from makeqr.enums import DataScheme
from makeqr.utils import make_link_data


class TelModel(
    QrDataBaseModel,
):
    tel: str

    @property
    def qr_data(self) -> str:
        return make_link_data(
            schema=DataScheme.TEL,
            link=self.tel,
        )
