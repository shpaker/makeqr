from typing import List, Optional

from makeqr.enums import DataScheme
from makeqr.models.base import QrDataBaseModel
from makeqr.utils import make_link_data

MECARD_SPECIAL_CHARACTERS: str = r'\;,:"'


class SmsModel(QrDataBaseModel):
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
