from pydantic import BaseModel, ConfigDict

from core.data_types import DatetimeStr


class Brand(BaseModel):
    name: str
    logo: str | None = None
    description: str | None = None
    status: int
    sort: int
    first_letter: str | None = None


class BrandSimpleOut(Brand):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr