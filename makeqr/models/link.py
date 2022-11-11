from click import types
from pydantic import AnyUrl, Field, validator

from makeqr.qr_data_model import QrDataBaseModel
from makeqr.utils import make_link_data

_DEFAULT_LINK_SCHEME = "https"


class QRLinkModel(
    QrDataBaseModel,
):
    url: AnyUrl = Field(
        alias="u",
        description="URL",
        click_type=types.STRING,
    )

    @property
    def qr_data(self) -> str:
        return make_link_data(
            link=self.url,
        )

    @classmethod
    @validator("url", pre=True)
    def url_validator(
        cls,
        value: str,
    ) -> str:
        if "://" not in value:
            return f"{_DEFAULT_LINK_SCHEME}://{value}"
        return value
