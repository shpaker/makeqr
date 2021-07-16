from typing import Optional, Tuple
from urllib.parse import quote

from pydantic import EmailStr, Field

from makeqr.enums import DataScheme
from makeqr.models.base import QrDataBaseModel

MECARD_SPECIAL_CHARACTERS: str = r'\;,:"'


class MailToModel(QrDataBaseModel):
    to: EmailStr
    subject: Optional[str] = Field(None, min_length=1)
    cc: Tuple[EmailStr, ...] = Field(default_factory=tuple)
    bcc: Tuple[EmailStr, ...] = Field(default_factory=tuple)
    body: Optional[str] = None

    @property
    def qr_data(self) -> str:
        data = f"{DataScheme.MAILTO}:{self.to}"
        args = list()
        if self.subject:
            args.append(f"subject={quote(self.subject)}")
        if self.cc:
            args.append(f'cc={quote(",".join(self.cc))}')
        if self.bcc:
            args.append(f'bcc={quote(",".join(self.bcc))}')
        if self.body:
            args.append(f"body={quote(self.body)}")
        return data if not args else f'{data}?{"&".join(args)}'
