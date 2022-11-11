from abc import ABC, abstractmethod

from pydantic import BaseModel, Extra


class QrDataBaseModel(
    ABC,
    BaseModel,
    extra=Extra.forbid,
):
    @property
    @abstractmethod
    def qr_data(self) -> str:
        raise NotImplementedError
