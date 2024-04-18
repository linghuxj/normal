from pydantic import BaseModel, ConfigDict

from . import GoodsIn, SpecValueIn, SpecValueOut
from core.data_types import DatetimeStr


class Product(BaseModel):
    name: str
    category_id: int
    brand_id: int
    image: str | None = None
    status: int
    detail: str | None = None


class ProductSimpleOut(Product):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr

    category: dict | None = None
    brand: dict | None = None


class ProductDetailOut(ProductSimpleOut):
    model_config = ConfigDict(from_attributes=True)

    parameters: list[SpecValueOut] | None = None
    goods: list[dict] | None = None


class ProductIn(BaseModel):
    name: str
    category_id: int
    brand_id: int
    image: str | None = None
    detail: str | None = None
    parameters: list[SpecValueIn] | None = None
    goods: list[GoodsIn] | None = None
