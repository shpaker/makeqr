from abc import ABC, abstractmethod

from pydantic import BaseModel, Extra

MECARD_SPECIAL_CHARACTERS: str = r'\;,:"'


class QrDataBaseModel(ABC, BaseModel, extra=Extra.forbid):
    @property
    @abstractmethod
    def qr_data(self) -> str:
        raise NotImplementedError
