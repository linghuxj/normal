# 数据库 增删改查
from typing import List, Any

from sqlalchemy import select, false
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.strategy_options import _AbstractLoad, joinedload

from core.exception import CustomException
from utils import status
from . import models, schemas, params
from core.crud import DalBase


class CategoryDal(DalBase):
    def __init__(self, db: AsyncSession):
        super(CategoryDal, self).__init__()
        self.db = db
        self.model = models.Category
        self.schema = schemas.CategorySimpleOut

    async def create_data(
            self,
            data: schemas.Category,
            options: List[_AbstractLoad] = None,
            return_obj: bool = False,
            schema: Any = None
    ) -> Any:
        """
        创建数据
        """
        unique = await self.get_data(name=data.name, return_none=True)
        if unique:
            raise CustomException(msg=f"{data.name} 已存在", code=status.HTTP_ERROR)
        if data.parent_id:
            parent = await self.get_data(id=data.parent_id, return_none=True)
            if not parent:
                raise CustomException(msg=f"父级分类不存在", code=status.HTTP_ERROR)
            if parent.level >= 3:
                raise CustomException(msg=f"最多只能创建三级分类", code=status.HTTP_ERROR)
            data.level = parent.level + 1
        else:
            data.level = 1
        # 佣金比例存在的情况下，其值不能小于0且不大于1
        if data.commission and (data.commission < 0 or data.commission > 1):
            raise CustomException(msg=f"佣金比例不能小于0或者大于1", code=status.HTTP_ERROR)
        return await super().create_data(data, options, return_obj, schema)

    async def put_data(
            self,
            data_id: int,
            data: Any,
            options: List[_AbstractLoad] = None,
            return_obj: bool = False,
            schema: Any = None
    ) -> Any:
        """
        修改数据
        """
        unique = await self.get_data(name=data.name, return_none=True)
        if unique and unique.id != data_id:
            raise CustomException(msg=f"{data.name} 已存在", code=status.HTTP_ERROR)
        if data.parent_id:
            parent = await self.get_data(id=data.parent_id, return_none=True)
            if not parent:
                raise CustomException(msg=f"父级分类不存在", code=status.HTTP_ERROR)
            if parent.level >= 3:
                raise CustomException(msg=f"最多只能创建三级分类", code=status.HTTP_ERROR)
            data.level = parent.level + 1
        else:
            data.level = 1
        # 佣金比例存在的情况下，其值不能小于0且不大于1
        if data.commission and (data.commission < 0 or data.commission > 1):
            raise CustomException(msg=f"佣金比例不能小于0或者大于1", code=status.HTTP_ERROR)
        return await super().put_data(data_id, data, options, return_obj, schema)

    async def get_tree_list(self, mode: int) -> list:
        """
        获取商品类型树列表

        :param mode:
        1：获取商品类型树列表
        2：获取商品类型树选择项，添加/修改商品类型时使用
        3：获取商品类型树列表，用户选择商品类型时使用

        :return: 商品类型树列表
        """
        if mode == 3:
            sql = select(self.model).where(self.model.status == 1, self.model.is_delete == false())
        else:
            sql = select(self.model).where(self.model.is_delete == false())
        queryset = await self.db.scalars(sql)
        datas = list(queryset.all())
        roots = filter(lambda i: not i.parent_id, datas)
        if mode == 1:
            categories = self.generate_tree_list(datas, roots)
        elif mode == 2 or mode == 3:
            categories = self.generate_tree_options(datas, roots)
        else:
            raise CustomException(msg=f"获取商品类型失败，无可用选项", code=400)
        return self.category_order(categories)

    def generate_tree_list(self, categories: list[models.Category], nodes: filter) -> list:
        """
        获取树形结构数据
        :param categories: 总商品类型列表
        :param nodes: 每层节点类型列表
        """
        data = []
        for root in nodes:
            router = schemas.CategoryTreeListOut.model_validate(root)
            sons = filter(lambda i: i.parent_id == root.id, categories)
            router.children = self.generate_tree_list(categories, sons)
            data.append(router.model_dump())
        return data

    def generate_tree_options(self, categories: list[models.Category], nodes: filter) -> list:
        """
        生成类型树选择项
        :param categories: 总类型列表
        :param nodes: 每层节点类型列表
        :return:
        """
        data = []
        for root in nodes:
            router = {"value": root.id, "label": root.name, "order": root.order}
            sons = filter(lambda i: i.parent_id == root.id, categories)
            router["children"] = self.generate_tree_options(categories, sons)
            data.append(router)
        return data

    @classmethod
    def category_order(cls, datas: list, order: str = "order", children: str = "children") -> list:
        """
        商品类型排序
        """
        result = sorted(datas, key=lambda category: category[order])
        for item in result:
            if item[children]:
                item[children] = sorted(item[children], key=lambda category: category[order])
        return result


class BrandDal(DalBase):
    def __init__(self, db: AsyncSession):
        super(BrandDal, self).__init__()
        self.db = db
        self.model = models.Brand
        self.schema = schemas.BrandSimpleOut

    async def create_data(
            self,
            data: schemas.Brand,
            options: List[_AbstractLoad] = None,
            return_obj: bool = False,
            schema: Any = None
    ) -> Any:
        """
        创建数据
        """
        unique = await self.get_data(name=data.name, return_none=True)
        if unique:
            raise CustomException(msg=f"{data.name} 已存在", code=status.HTTP_ERROR)
        return await super().create_data(data, options, return_obj, schema)

    async def put_data(
            self,
            data_id: int,
            data: Any,
            options: List[_AbstractLoad] = None,
            return_obj: bool = False,
            schema: Any = None
    ) -> Any:
        """
        修改数据
        """
        unique = await self.get_data(name=data.name, return_none=True)
        if unique and unique.id != data_id:
            raise CustomException(msg=f"{data.name} 已存在", code=status.HTTP_ERROR)
        return await super().put_data(data_id, data, options, return_obj, schema)


class GoodsDal(DalBase):
    def __init__(self, db: AsyncSession):
        super(GoodsDal, self).__init__()
        self.db = db
        self.model = models.Goods
        self.schema = schemas.GoodsSimpleOut

    async def create_data(
            self,
            data: schemas.GoodsIn,
            options: List[_AbstractLoad] = None,
            return_obj: bool = False,
            schema: Any = None
    ) -> Any:
        """
        创建数据
        """
        # 商品价格和售价不能小于等于0
        if data.price.price <= 0 or data.price.cost <= 0:
            raise CustomException(msg=f"商品价格和售价不能小于等于0", code=status.HTTP_ERROR)
        # 库存不能小于等于0
        if data.price.stock <= 0:
            raise CustomException(msg=f"库存不能小于等于0", code=status.HTTP_ERROR)
        # 商品规格值不能重复
        spec_values = set()
        for spec in data.specs:
            if not spec.name or not spec.value:
                raise CustomException(msg=f"规格名称和规格值不能为空", code=status.HTTP_ERROR)
            if spec.value in spec_values:
                raise CustomException(msg=f"商品规格值不能重复", code=status.HTTP_ERROR)
            spec_values.add(spec.value)

        # 复制商品基本信息
        goods = self.model(**data.model_dump())
        # 复制商品价格信息
        goods.goods_price = models.Price(**data.price.model_dump())
        # 复制商品积分信息
        if data.goods_integral:
            goods.goods_integral = models.Integral(**data.integral.model_dump())
        # 复制商品规格信息
        goods.goods_spec_values = [models.SpecValue(**spec.model_dump()) for spec in data.specs]
        await self.flush(goods)
        return await self.out_dict(goods, options, return_obj, schema)

    async def put_data(
            self,
            data_id: int,
            data: schemas.GoodsUpdate,
            options: List[_AbstractLoad] = None,
            return_obj: bool = False,
            schema: Any = None
    ) -> Any:
        """
        修改数据
        """
        # 判断商品是否存在
        goods = await self.get_data(
            data_id=data_id,
            options=[joinedload(self.model.goods_price, self.model.goods_integral, self.model.goods_spec_values)],
            return_none=True)
        if not goods:
            raise CustomException(msg=f"商品不存在", code=status.HTTP_ERROR)
        if data.goods_price:
            # 商品价格存在，且判断修改后的价格是否大于0，是的话更新原商品价格，否则抛出异常，提示价格不能小于等于0
            if data.goods_price.price:
                self.check_value(data.goods_price.price, "商品售价")
                goods.goods_price.price = data.goods_price.price
            # 商品成本价存在，且判断修改后的成本价是否大于0，是的话更新原商品成本价，否则抛出异常，提示成本价不能小于等于0
            if data.goods_price.cost:
                self.check_value(data.goods_price.cost, "商品成本价")
                goods.goods_price.cost = data.goods_price.cost
            # 商品库存存在，且判断修改后的库存是否大于0，是的话更新原商品库存，否则抛出异常，提示库存不能小于等于0
            if data.goods_price.stock:
                self.check_value(data.goods_price.stock, "商品库存")
                goods.goods_price.stock = data.goods_price.stock
        if data.goods_integral:
            # 商品积分存在，且判断修改后的积分是否大于0，是的话更新原商品积分，否则抛出异常，提示积分不能小于等于0
            if data.goods_integral.integral:
                self.check_value(data.goods_integral.integral, "商品积分")
                goods.goods_integral.integral = data.goods_integral.integral
            # 商品积分外价格存在，且判断修改后的积分外价格是否大于0，是的话更新原商品积分外价格，否则抛出异常，提示积分外价格不能小于等于0
            if data.goods_integral.price:
                self.check_value(data.goods_integral.price, "商品积分外价格")
                goods.goods_integral.price = data.goods_integral.price
            # 商品积分库存存在，且判断修改后的积分库存是否大于0，是的话更新原商品积分库存，否则抛出异常，提示积分库存不能小于等于0
            if data.goods_integral.stock:
                self.check_value(data.goods_integral.stock, "商品积分库存")
                goods.goods_integral.stock = data.goods_integral.stock
        if data.goods_spec_values:
            # 更新商品规格值
            goods.goods_spec_values = [models.SpecValue(**spec.model_dump()) for spec in data.goods_spec_values]

        # 更新商品及相关信息
        await self.flush(goods)
        return await self.out_dict(data, None, return_obj, schema)

    async def goods_change_status(self, data_id: int, status: int):
        pass

    @classmethod
    def check_value(cls, value: float, name: str):
        """
        检查值是否大于0
        """
        if value and value <= 0:
            raise CustomException(msg=f"{name}不能小于等于0", code=status.HTTP_ERROR)

    @classmethod
    def check_spec_value(cls, goods_spec_values: list[schemas.SpecValueIn]):
        """  dd11x
        检查规格名称和规格值是否存在，同时检查规格值是否重复
        """
        spec_values = set()
        for spec in goods_spec_values:
            if not spec.name or not spec.value:
                raise CustomException(msg=f"规格名称和规格值不能为空", code=status.HTTP_ERROR)
            if spec.value in spec_values:
                raise CustomException(msg=f"商品规格值不能重复", code=status.HTTP_ERROR)
            spec_values.add(spec.value)
