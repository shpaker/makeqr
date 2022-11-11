from typing import Optional, Tuple
from urllib.parse import quote

from pydantic import EmailStr, Field

from makeqr.constants import DataScheme
from makeqr.qr_data_model import QrDataBaseModel


class QRMailToModel(
    QrDataBaseModel,
):
    to: EmailStr = Field(
        description="Recipient",
        alias="t",
    )
    subject: Optional[str] = Field(
        None,
        alias="s",
    )
    cc: Tuple[EmailStr, ...] = Field(
        (),
        description="Carbon copy",
        click_option_multiple=True,
    )
    bcc: Tuple[EmailStr, ...] = Field(
        (),
        description="Blind carbon copy",
        click_option_multiple=True,
    )
    body: Optional[str] = Field(
        None,
        description="E-mail body",
        alias="b",
    )

    @property
    def qr_data(self) -> str:
        data = f"{DataScheme.MAILTO}:{self.to}"
        args = []
        if self.subject:
            args.append(f"subject={quote(self.subject)}")
        if self.cc:
            args.append(f'cc={quote(",".join(self.cc))}')
        if self.bcc:
            args.append(f'bcc={quote(",".join(self.bcc))}')
        if self.body:
            args.append(f"body={quote(self.body)}")
        return data if not args else f'{data}?{"&".join(args)}'
