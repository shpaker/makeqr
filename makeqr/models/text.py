from pydantic import Field

from makeqr.qr_data_model import QrDataBaseModel


class QRTextModel(
    QrDataBaseModel,
):
    text: str = Field(
        False,
        alias="t",
    )

    @property
    def qr_data(self) -> str:
        return self.text
