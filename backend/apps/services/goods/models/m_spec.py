# 商品规格表
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from apps.services.goods.models import Category, Goods
from db.db_base import BaseModel


class Spec(BaseModel):
    """
    商品规格表：
    包含：商品规格名称、商品规格类型、商品规格排序、商品规格状态、所属分类、商品规格默认值
    """
    __tablename__ = "goods_spec"
    __table_args__ = ({'comment': '商品规格表'})

    name: Mapped[str] = mapped_column(String(50), nullable=False, comment="商品规格名称")
    sort: Mapped[int] = mapped_column(Integer, default=0, comment="商品规格排序")
    status: Mapped[int] = mapped_column(Integer, default=1, comment="商品规格状态")
    default_value: Mapped[str | None] = mapped_column(String(255), comment="商品规格默认值")

    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("goods_category.id", ondelete="RESTRICT"),
        comment="所属分类"
    )
    category: Mapped[Category] = relationship(foreign_keys=category_id)

    spec_values: Mapped[list["SpecValue"]] = relationship(back_populates="spec")


class SpecValue(BaseModel):
    """
    商品规格值表：
    包含：商品规格值、商品规格值排序、商品规格值状态、所属规格
    """
    __tablename__ = "goods_spec_value"
    __table_args__ = ({'comment': '商品规格值表'})

    spec_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("goods_spec.id", ondelete="CASCADE"),
        comment="所属规格"
    )
    spec: Mapped[list["Spec"]] = relationship(foreign_keys=spec_id, back_populates="spec_values")

    goods_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("goods_goods.id", ondelete="CASCADE"),
        comment="所属商品"
    )
    goods: Mapped[list["Goods"]] = relationship(foreign_keys=goods_id, back_populates="goods_spec_values")

    value: Mapped[str] = mapped_column(String(50), nullable=False, comment="商品规格值")
    sort: Mapped[int] = mapped_column(Integer, default=0, comment="商品规格值排序")
    status: Mapped[int] = mapped_column(Integer, default=1, comment="商品规格值状态")
