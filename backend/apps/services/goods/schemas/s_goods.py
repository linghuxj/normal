from pydantic import BaseModel, ConfigDict

from apps.services.goods.schemas import SpecValueIn, SpecValueOut, PriceOut, PriceIn, IntegralOut, IntegralIn
from core.data_types import DatetimeStr


class Goods(BaseModel):
    name: str
    image: str | None = None
    status: int
    detail: str | None = None
    product_id: int


class GoodsSimpleOut(Goods):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr

    goods_price: PriceOut
    goods_integral: IntegralOut | None = None
    goods_spec_values: list[SpecValueOut]


class GoodsIn(BaseModel):
    name: str
    images: list[str]
    detail: str | None = None
    goods_price: PriceIn
    goods_integral: IntegralIn | None = None
    goods_spec_values: list[SpecValueIn]


class GoodsUpdate(BaseModel):
    name: str | None = None
    images: list[str] = []
    status: int | None = None
    detail: str | None = None
    goods_price: PriceIn
    goods_integral: IntegralIn | None = None
    goods_spec_values: list[SpecValueIn] = []
