# Desc: 商品图片表
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.db_base import BaseModel


class Images(BaseModel):
    """
    商品图片表：
    包含：图片地址、图片排序、所属商品
    """
    __tablename__ = "goods_images"
    __table_args__ = ({'comment': '商品图片表'})

    image: Mapped[str] = mapped_column(String(500), nullable=False, comment="图片地址")
    sort: Mapped[int] = mapped_column(Integer, default=0, comment="图片排序")

    goods_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("goods_goods.id", ondelete="CASCADE"),
        comment="所属商品"
    )
