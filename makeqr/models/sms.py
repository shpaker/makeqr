from typing import List, Optional

from makeqr.base import QrDataBaseModel
from makeqr.enums import DataScheme
from makeqr.utils import make_link_data


class SmsModel(
    QrDataBaseModel,
):
    recipients: Optional[List[str]] = None
    body: Optional[str] = None

    @property
    def qr_data(self) -> str:
        body_dict = dict(body=self.body) if self.body else dict()
        return make_link_data(
            schema=DataScheme.SMS,
            link=self.recipients,
            params=body_dict,
        )
