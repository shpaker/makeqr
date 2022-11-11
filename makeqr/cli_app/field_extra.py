from click import types
from pydantic import BaseModel


class FieldExtraClickOptionsModel(BaseModel, arbitrary_types_allowed=True):
    click_option_type: types.ParamType = types.STRING
    click_option_multiple: bool = False
