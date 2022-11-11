from typing import Optional, Tuple

from pydantic import Field

from makeqr.constants import DataScheme
from makeqr.qr_data_model import QrDataBaseModel
from makeqr.utils import make_link_data


class QRSMSModel(
    QrDataBaseModel,
):
    recipients: Tuple[str, ...] = Field(
        [],
        alias="r",
        click_option_multiple=True,
    )
    body: Optional[str] = Field(
        None,
        alias="b",
    )

    @property
    def qr_data(self) -> str:
        body_dict = {"body": self.body} if self.body else {}
        return make_link_data(
            schema=DataScheme.SMS,
            link=self.recipients,
            params=body_dict,
        )
