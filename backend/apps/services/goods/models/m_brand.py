# 商品品牌表
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from db.db_base import BaseModel


class Brand(BaseModel):
    """
    商品品牌表：
    包含：品牌名称、品牌logo、品牌描述、品牌状态、品牌排序、品牌首字母
    """
    __tablename__ = "goods_brand"
    __table_args__ = ({'comment': '商品品牌表'})

    name: Mapped[str] = mapped_column(String(50), nullable=False, comment="品牌名称")
    logo: Mapped[str | None] = mapped_column(String(500), comment="品牌logo")
    description: Mapped[str | None] = mapped_column(String(255), comment="品牌描述")
    status: Mapped[int] = mapped_column(Integer, default=1, comment="品牌状态")
    sort: Mapped[int] = mapped_column(Integer, default=0, comment="品牌排序")
    first_letter: Mapped[str | None] = mapped_column(String(1), comment="品牌首字母")
