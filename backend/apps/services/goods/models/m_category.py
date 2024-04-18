# 商品类型表
from sqlalchemy import String, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.db_base import BaseModel


class Category(BaseModel):
    """
    商品类型表：
    包含：商品类型名称、商品类型描述、商品类型图片、商品类型状态、商品类型排序、佣金比例、分层级别、上级商品类型
    """
    __tablename__ = "goods_category"
    __table_args__ = ({'comment': '商品类型表'})

    name: Mapped[str] = mapped_column(String(50), nullable=False, comment="商品类型名称")
    description: Mapped[str | None] = mapped_column(String(255), comment="商品类型描述")
    image: Mapped[str | None] = mapped_column(String(500), comment="商品类型图片")
    status: Mapped[int] = mapped_column(Integer, default=1, comment="商品类型状态")
    sort: Mapped[int] = mapped_column(Integer, default=0, comment="商品类型排序")
    commission: Mapped[float] = mapped_column(Float, default=0, comment="佣金比例")
    level: Mapped[int] = mapped_column(Integer, default=1, comment="分层级别")

    parent_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("goods_category.id", ondelete='CASCADE'),
        comment="上级商品类型"
    )
