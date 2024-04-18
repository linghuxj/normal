from typing import List

from pydantic import BaseModel, ConfigDict

from core.data_types import DatetimeStr


class Category(BaseModel):
    name: str
    status: int
    sort: int
    description: str | None = None
    image: str | None = None
    commission: float
    level: int
    parent_id: int = None


class CategorySimpleOut(Category):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr


class CategoryTreeListOut(CategorySimpleOut):
    model_config = ConfigDict(from_attributes=True)

    children: List[dict] = []
