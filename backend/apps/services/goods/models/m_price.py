# 商品价格表
from sqlalchemy import Float, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.services.goods.models import Goods
from db.db_base import BaseModel


class Price(BaseModel):
    """
    商品价格表：
    包含：商品销售价格、商品成本价、商品库存量、所属商品
    """
    __tablename__ = "goods_price"
    __table_args__ = ({'comment': '商品价格表'})

    price: Mapped[float] = mapped_column(Float, nullable=False, comment="商品销售价格")
    cost: Mapped[float | None] = mapped_column(Float, comment="商品成本价")
    stock: Mapped[int] = mapped_column(Integer, default=0, comment="商品库存量")

    goods_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("goods_goods.id", ondelete="CASCADE"),
        comment="所属商品"
    )
    goods: Mapped[Goods] = relationship(foreign_keys=goods_id, back_populates="goods_price")


class Integral(BaseModel):
    """
    商品积分表：
    包含：商品积分、商品积分外价格、商品库存量、所属商品
    """
    __tablename__ = "goods_integral"
    __table_args__ = ({'comment': '商品积分表'})

    integral: Mapped[int] = mapped_column(Integer, nullable=False, comment="商品积分")
    price: Mapped[float | None] = mapped_column(Float, comment="商品积分外价格")
    stock: Mapped[int] = mapped_column(Integer, default=0, comment="商品库存量")

    goods_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("goods_goods.id", ondelete="CASCADE"),
        comment="所属商品"
    )
    goods: Mapped[Goods] = relationship(foreign_keys=goods_id, back_populates="goods_integral")
