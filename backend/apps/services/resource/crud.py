# 数据库 增删改查操作

from sqlalchemy.ext.asyncio import AsyncSession
from core.crud import DalBase
from . import models, schemas


class ImagesDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(ImagesDal, self).__init__()
        self.db = db
        self.model = models.Images
        self.schema = schemas.ImagesSimpleOut
