from makeqr.enums import DataScheme
from makeqr.models.base import QrDataBaseModel
from makeqr.utils import make_link_data

MECARD_SPECIAL_CHARACTERS: str = r'\;,:"'


class TelModel(QrDataBaseModel):
    tel: str

    @property
    def qr_data(self) -> str:
        return make_link_data(
            schema=DataScheme.TEL,
            link=self.tel,
        )
