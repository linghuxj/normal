# 产品参数表
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from apps.services.goods.models import Product, Category
from db.db_base import BaseModel


class Param(BaseModel):
    """
    产品参数表：
    包含：产品参数名称、产品参数类型、产品参数排序、产品参数状态、所属分类、产品参数默认值
    """
    __tablename__ = "product_param"
    __table_args__ = ({'comment': '产品参数表'})

    name: Mapped[str] = mapped_column(String(50), nullable=False, comment="产品参数名称")
    sort: Mapped[int] = mapped_column(Integer, default=0, comment="产品参数排序")
    status: Mapped[int] = mapped_column(Integer, default=1, comment="产品参数状态")
    default_value: Mapped[str | None] = mapped_column(String(255), comment="产品参数默认值")

    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("product_category.id", ondelete="RESTRICT"),
        comment="所属分类"
    )
    category: Mapped[Category] = relationship(foreign_keys=category_id)

    param_values: Mapped[list["ParamValue"]] = relationship(back_populates="param")


class ParamValue(BaseModel):
    """
    产品参数值表：
    包含：产品参数值、产品参数值排序、产品参数值状态、所属参数
    """
    __tablename__ = "product_param_value"
    __table_args__ = ({'comment': '产品参数值表'})

    param_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("product_param.id", ondelete="CASCADE"),
        comment="所属参数"
    )
    param: Mapped[list["param"]] = relationship(foreign_keys=param_id, back_populates="param_values")

    product_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("product_product.id", ondelete="CASCADE"),
        comment="所属产品"
    )
    product: Mapped[list["Product"]] = relationship(foreign_keys=product_id, back_populates="product_param_values")

    value: Mapped[str] = mapped_column(String(50), nullable=False, comment="产品参数值")
    sort: Mapped[int] = mapped_column(Integer, default=0, comment="产品参数值排序")
    status: Mapped[int] = mapped_column(Integer, default=1, comment="产品参数值状态")
