from pydantic import BaseModel, ConfigDict

from core.data_types import DatetimeStr


class Spec(BaseModel):
    name: str
    type: int
    sort: int
    status: int
    default_value: str | None = None
    category_id: int


class SpecSimpleOut(Spec):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr


class SpecValueOut(BaseModel):
    id: int
    name: str
    spec_id: int
    value: str


class SpecValueIn(BaseModel):
    name: str
    spec_id: int | None = None
    value: str
