# 商品相关表
from sqlalchemy import String, Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.services.auth.models import User
from apps.services.goods.models import SpecValue, Price, Integral, Category, Brand
from apps.services.goods.models.m_param import ParamValue
from db.db_base import BaseModel


class Product(BaseModel):
    """
    产品表：
    包含：产品名称、所属分类、所属品牌、产品图片、产品状态、产品参数、产品详情、所属商品
    """
    __tablename__ = "goods_product"
    __table_args__ = ({'comment': '产品表'})

    name: Mapped[str] = mapped_column(String(50), nullable=False, comment="产品名称")
    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("goods_category.id", ondelete="CASCADE"),
        comment="所属分类"
    )
    category: Mapped["Category"] = relationship(foreign_keys=category_id)

    brand_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("goods_brand.id", ondelete="CASCADE"),
        comment="所属品牌"
    )
    brand: Mapped["Brand"] = relationship(foreign_keys=brand_id)

    image: Mapped[str | None] = mapped_column(String(500), comment="产品图片")
    status: Mapped[int] = mapped_column(Integer, default=1, comment="产品状态")
    detail: Mapped[str | None] = mapped_column(Text, comment="产品详情")

    product_param_values: Mapped[list["ParamValue"]] = relationship(back_populates="product")

    create_user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("auth_user.id", ondelete='RESTRICT'),
        comment="创建人"
    )
    create_user: Mapped[User] = relationship(foreign_keys=create_user_id)


class Goods(BaseModel):
    """
    商品表：
    包含：商品名称、商品图片、商品状态、商品详情、商品规格、所属产品
    """
    __tablename__ = "goods_goods"
    __table_args__ = ({'comment': '商品表'})

    name: Mapped[str] = mapped_column(String(50), nullable=False, comment="商品名称")
    image: Mapped[str | None] = mapped_column(String(500), comment="商品图片")
    status: Mapped[int] = mapped_column(Integer, default=1, comment="商品状态")
    detail: Mapped[str | None] = mapped_column(Text, comment="商品详情")

    product_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("goods_product.id", ondelete="CASCADE"),
        comment="所属产品"
    )
    product: Mapped[Product] = relationship(foreign_keys=product_id)

    goods_spec_values: Mapped[list["SpecValue"]] = relationship(back_populates="goods")

    goods_price: Mapped[Price] = relationship(back_populates="goods")
    goods_integral: Mapped[Integral] = relationship(back_populates="goods")

    create_user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("auth_user.id", ondelete='RESTRICT'),
        comment="创建人"
    )
    create_user: Mapped[User] = relationship(foreign_keys=create_user_id)
