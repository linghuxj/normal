from pydantic import BaseModel, ConfigDict


class Price(BaseModel):
    price: float
    cost: float
    stock: int


class PriceOut(Price):
    model_config = ConfigDict(from_attributes=True)

    id: int


class PriceIn(Price):
    model_config = ConfigDict(from_attributes=True)


class Integral(BaseModel):
    price: float
    integral: int
    stock: int


class IntegralOut(Integral):
    model_config = ConfigDict(from_attributes=True)

    id: int


class IntegralIn(Price):
    model_config = ConfigDict(from_attributes=True)
