from core.database import Base
from sqlalchemy import ForeignKey, Column, Table, Integer

goods_category_brand = Table(
    "goods_category_brand",
    Base.metadata,
    Column("category_id", Integer, ForeignKey("goods_category.id", ondelete="CASCADE")),
    Column("brand_id", Integer, ForeignKey("goods_brand.id", ondelete="CASCADE")),
)
