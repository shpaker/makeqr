from typing import Any, Dict, Optional

from pydantic import AnyUrl

from makeqr.models.base import QrDataBaseModel
from makeqr.utils import make_link_data

MECARD_SPECIAL_CHARACTERS: str = r'\;,:"'


class LinkModel(QrDataBaseModel):
    url: AnyUrl
    params: Optional[Dict[str, Any]] = None

    @property
    def qr_data(self) -> str:
        return make_link_data(
            link=self.url,
            params=self.params,
        )
