# 数据库 增删改查操作

# sqlalchemy 官方文档：https://docs.sqlalchemy.org/en/20/index.html
# sqlalchemy 查询操作（官方文档）: https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html
# sqlalchemy 增删改操作：https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html
# sqlalchemy 1.x 语法迁移到 2.x :https://docs.sqlalchemy.org/en/20/changelog/migration_20.html#migration-20-query-usage

import datetime
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, delete, update, BinaryExpression, ScalarResult, select, false, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.orm.strategy_options import _AbstractLoad
from starlette import status
from core.exception import CustomException
from sqlalchemy.sql.selectable import Select as SelectType
from typing import Any, List, Union


class DalBase:
    # 倒叙
    ORDER_FIELD = ["desc", "descending"]

    def __init__(self, db: AsyncSession = None, model: Any = None, schema: Any = None):
        self.db = db
        self.model = model
        self.schema = schema

    async def get_data(
            self,
            data_id: int = None,
            start_sql: SelectType = None,
            select_from: List[Any] = None,
            join: List[Any] = None,
            outer_join: List[Any] = None,
            options: List[_AbstractLoad] = None,
            where: List[BinaryExpression] = None,
            order: str = None,
            order_field: str = None,
            return_none: bool = False,
            schema: Any = None,
            **kwargs
    ) -> Any:
        """
        获取单个数据，默认使用 ID 查询，否则使用关键词查询

        :param data_id: 数据 ID
        :param start_sql: 初始 sql
        :param select_from: 用于指定查询从哪个表开始，通常与 .join() 等方法一起使用。
        :param join: 创建内连接（INNER JOIN）操作，返回两个表中满足连接条件的交集。
        :param outer_join: 用于创建外连接（OUTER JOIN）操作，返回两个表中满足连接条件的并集，包括未匹配的行，并用 NULL 值填充。
        :param options: 用于为查询添加附加选项，如预加载、延迟加载等。
        :param where: 当前表查询条件，原始表达式
        :param order: 排序，默认正序，为 desc 是倒叙
        :param order_field: 排序字段
        :param return_none: 是否返回空 None，否认 抛出异常，默认抛出异常
        :param schema: 指定使用的序列化对象
        :param kwargs: 查询参数
        :return: 默认返回 ORM 对象，如果存在 schema 则会返回 schema 结果
        """
        if not isinstance(start_sql, SelectType):
            start_sql = select(self.model).where(self.model.is_delete == false())

        if data_id is not None:
            start_sql = start_sql.where(self.model.id == data_id)

        queryset: ScalarResult = await self.filter_core(
            start_sql=start_sql,
            select_from=select_from,
            join=join,
            outer_join=outer_join,
            options=options,
            where=where,
            order=order,
            order_field=order_field,
            return_sql=False,
            **kwargs
        )

        if options:
            data = queryset.unique().first()
        else:
            data = queryset.first()

        if not data and return_none:
            return None

        if data and schema:
            return schema.model_validate(data).model_dump()

        if data:
            return data

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="未找到此数据")

    async def get_datas(
            self,
            page: int = 1,
            limit: int = 10,
            start_sql: SelectType = None,
            select_from: List[Any] = None,
            join: List[Any] = None,
            outer_join: List[Any] = None,
            options: List[_AbstractLoad] = None,
            where: List[BinaryExpression] = None,
            order: str = None,
            order_field: str = None,
            return_count: bool = False,
            return_scalars: bool = False,
            return_objs: bool = False,
            schema: Any = None,
            distinct: bool = False,
            **kwargs
    ) -> Union[List[Any], ScalarResult, tuple]:
        """
        获取数据列表

        :param page: 页码
        :param limit: 当前页数据量
        :param start_sql: 初始 sql
        :param select_from: 用于指定查询从哪个表开始，通常与 .join() 等方法一起使用。
        :param join: 创建内连接（INNER JOIN）操作，返回两个表中满足连接条件的交集。
        :param outer_join: 用于创建外连接（OUTER JOIN）操作，返回两个表中满足连接条件的并集，包括未匹配的行，并用 NULL 值填充。
        :param options: 用于为查询添加附加选项，如预加载、延迟加载等。
        :param where: 当前表查询条件，原始表达式
        :param order: 排序，默认正序，为 desc 是倒叙
        :param order_field: 排序字段
        :param return_count: 默认为 False，是否返回 count 过滤后的数据总数，不会影响其他返回结果，会一起返回为一个数组
        :param return_scalars: 返回scalars后的结果
        :param return_objs: 是否返回对象
        :param schema: 指定使用的序列化对象
        :param distinct: 是否结果去重
        :param kwargs: 查询参数，使用的是自定义表达式
        :return: 返回值优先级：return_scalars > return_objs > schema
        """
        sql: SelectType = await self.filter_core(
            start_sql=start_sql,
            select_from=select_from,
            join=join,
            outer_join=outer_join,
            options=options,
            where=where,
            order=order,
            order_field=order_field,
            return_sql=True,
            **kwargs
        )

        if distinct:
            sql = sql.distinct()

        count = 0
        if return_count:
            count_sql = select(func.count()).select_from(sql.alias())
            count_queryset = await self.db.execute(count_sql)
            count = count_queryset.one()[0]

        if limit != 0:
            sql = sql.offset((page - 1) * limit).limit(limit)

        queryset = await self.db.scalars(sql)

        if return_scalars:
            if return_count:
                return queryset, count
            return queryset

        if options:
            result = queryset.unique().all()
        else:
            result = queryset.all()

        if return_objs:
            if return_count:
                return list(result), count
            return list(result)

        datas = [await self.out_dict(i, schema=schema) for i in result]
        if return_count:
            return datas, count
        return datas

    async def get_count(
            self,
            select_from: List[Any] = None,
            join: List[Any] = None,
            outer_join: List[Any] = None,
            where: List[BinaryExpression] = None,
            **kwargs
    ) -> int:
        """
        获取数据总数

        :param select_from: 用于指定查询从哪个表开始，通常与 .join() 等方法一起使用。
        :param join: 创建内连接（INNER JOIN）操作，返回两个表中满足连接条件的交集。
        :param outer_join: 用于创建外连接（OUTER JOIN）操作，返回两个表中满足连接条件的并集，包括未匹配的行，并用 NULL 值填充。
        :param where: 当前表查询条件，原始表达式
        :param kwargs: 查询参数
        """
        start_sql = select(func.count(self.model.id))
        sql = await self.filter_core(
            start_sql=start_sql,
            select_from=select_from,
            join=join,
            outer_join=outer_join,
            where=where,
            return_sql=True,
            **kwargs
        )
        queryset = await self.db.execute(sql)
        return queryset.one()[0]

    async def create_data(
            self,
            data,
            options: List[_AbstractLoad] = None,
            return_obj: bool = False,
            schema: Any = None
    ) -> Any:
        """
        创建单个数据
        :param data: 创建数据
        :param options: 指示应使用select在预加载中加载给定的属性。
        :param schema: ，指定使用的序列化对象
        :param return_obj: ，是否返回对象
        """
        if isinstance(data, dict):
            obj = self.model(**data)
        else:
            obj = self.model(**data.model_dump())
        await self.flush(obj)
        return await self.out_dict(obj, options, return_obj, schema)

    async def create_datas(self, datas: List[dict]) -> None:
        """
        批量创建数据
        SQLAlchemy 2.0 批量插入不支持 MySQL 返回值：
        https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#getting-new-objects-with-returning

        :param datas: 字典数据列表
        """
        await self.db.execute(insert(self.model), datas)
        await self.db.flush()

    async def put_data(
            self,
            data_id: int,
            data: Any,
            options: List[_AbstractLoad] = None,
            return_obj: bool = False,
            schema: Any = None
    ) -> Any:
        """
        更新单个数据
        :param data_id: 修改行数据的 ID
        :param data: 数据内容
        :param options: 指示应使用select在预加载中加载给定的属性。
        :param return_obj: ，是否返回对象
        :param schema: ，指定使用的序列化对象
        """
        obj = await self.get_data(data_id, options=options)
        obj_dict = jsonable_encoder(data)
        for key, value in obj_dict.items():
            setattr(obj, key, value)
        await self.flush(obj)
        return await self.out_dict(obj, None, return_obj, schema)

    async def delete_datas(self, ids: List[int], soft: bool = False, **kwargs) -> None:
        """
        删除多条数据
        :param ids: 数据集
        :param soft: 是否执行软删除
        :param kwargs: 其他更新字段
        """
        if soft:
            await self.db.execute(
                update(self.model).where(self.model.id.in_(ids)).values(
                    delete_datetime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    is_delete=True,
                    **kwargs
                )
            )
        else:
            await self.db.execute(delete(self.model).where(self.model.id.in_(ids)))
        await self.flush()

    async def flush(self, obj: Any = None) -> Any:
        """
        刷新到数据库
        :param obj:
        :return:
        """
        if obj:
            self.db.add(obj)
        await self.db.flush()
        if obj:
            # 使用 get_data 或者 get_datas 获取到实例后如何更新了实例，并需要序列化实例，那么需要执行 refresh 刷新才能正常序列化
            await self.db.refresh(obj)
        return obj

    async def out_dict(
            self,
            obj: Any,
            options: List[_AbstractLoad] = None,
            return_obj: bool = False,
            schema: Any = None
    ) -> Any:
        """
        序列化
        :param obj:
        :param options: 指示应使用select在预加载中加载给定的属性。
        :param return_obj: ，是否返回对象
        :param schema: ，指定使用的序列化对象
        :return:
        """
        if options:
            obj = await self.get_data(obj.id, options=options)
        if return_obj:
            return obj
        if schema:
            return schema.model_validate(obj).model_dump()
        return self.schema.model_validate(obj).model_dump()

    async def filter_core(
            self,
            start_sql: SelectType = None,
            select_from: List[Any] = None,
            join: List[Any] = None,
            outer_join: List[Any] = None,
            options: List[_AbstractLoad] = None,
            where: List[BinaryExpression] = None,
            order: str = None,
            order_field: str = None,
            return_sql: bool = False,
            **kwargs
    ) -> Union[ScalarResult, SelectType]:
        """
        数据过滤核心功能

        :param start_sql: 初始 sql
        :param select_from: 用于指定查询从哪个表开始，通常与 .join() 等方法一起使用。
        :param join: 创建内连接（INNER JOIN）操作，返回两个表中满足连接条件的交集。
        :param outer_join: 用于创建外连接（OUTER JOIN）操作，返回两个表中满足连接条件的并集，包括未匹配的行，并用 NULL 值填充。
        :param options: 用于为查询添加附加选项，如预加载、延迟加载等。
        :param where: 当前表查询条件，原始表达式
        :param order: 排序，默认正序，为 desc 是倒叙
        :param order_field: 排序字段
        :param return_sql: 是否直接返回 sql
        :return: 返回过滤后的总数居 或 sql
        """
        if not isinstance(start_sql, SelectType):
            start_sql = select(self.model).where(self.model.is_delete == false())

        sql = self.add_relation(
            start_sql=start_sql,
            select_from=select_from,
            join=join,
            outer_join=outer_join,
            options=options
        )

        if where:
            sql = sql.where(*where)

        sql = self.add_filter_condition(sql, **kwargs)

        if order_field and (order in self.ORDER_FIELD):
            sql = sql.order_by(getattr(self.model, order_field).desc(), self.model.id.desc())
        elif order_field:
            sql = sql.order_by(getattr(self.model, order_field), self.model.id)
        elif order in self.ORDER_FIELD:
            sql = sql.order_by(self.model.id.desc())

        if return_sql:
            return sql

        queryset = await self.db.scalars(sql)

        return queryset

    def add_relation(
            self,
            start_sql: SelectType,
            select_from: List[Any] = None,
            join: List[Any] = None,
            outer_join: List[Any] = None,
            options: List[_AbstractLoad] = None,
    ) -> SelectType:
        """
        :param start_sql: 初始 sql
        :param select_from: 用于指定查询从哪个表开始，通常与 .join() 等方法一起使用。
        :param join: 创建内连接（INNER JOIN）操作，返回两个表中满足连接条件的交集。
        :param outer_join: 用于创建外连接（OUTER JOIN）操作，返回两个表中满足连接条件的并集，包括未匹配的行，并用 NULL 值填充。
        :param options: 用于为查询添加附加选项，如预加载、延迟加载等。
        """
        if select_from:
            start_sql = start_sql.select_from(*select_from)

        if join:
            for relation in join:
                table = relation[0]
                if isinstance(table, str):
                    table = getattr(self.model, table)
                if len(relation) == 2:
                    start_sql = start_sql.join(table, relation[1])
                else:
                    start_sql = start_sql.join(table)

        if outer_join:
            for relation in outer_join:
                table = relation[0]
                if isinstance(table, str):
                    table = getattr(self.model, table)
                if len(relation) == 2:
                    start_sql = start_sql.outerjoin(table, relation[1])
                else:
                    start_sql = start_sql.outerjoin(table)

        if options:
            start_sql = start_sql.options(*options)

        return start_sql

    def add_filter_condition(self, sql: SelectType, **kwargs) -> SelectType:
        """
        添加过滤条件
        :param sql:
        :param kwargs: 关键词参数
        """
        conditions = self.__dict_filter(**kwargs)
        if conditions:
            sql = sql.where(*conditions)
        return sql

    def __dict_filter(self, **kwargs) -> List[BinaryExpression]:
        """
        字典过滤
        :param model:
        :param kwargs:
        """
        conditions = []
        for field, value in kwargs.items():
            if value is not None and value != "":
                attr = getattr(self.model, field)
                if isinstance(value, tuple):
                    if len(value) == 1:
                        if value[0] == "None":
                            conditions.append(attr.is_(None))
                        elif value[0] == "not None":
                            conditions.append(attr.isnot(None))
                        else:
                            raise CustomException("SQL查询语法错误")
                    elif len(value) == 2 and value[1] not in [None, [], ""]:
                        if value[0] == "date":
                            # 根据日期查询， 关键函数是：func.time_format和func.date_format
                            conditions.append(func.date_format(attr, "%Y-%m-%d") == value[1])
                        elif value[0] == "like":
                            conditions.append(attr.like(f"%{value[1]}%"))
                        elif value[0] == "in":
                            conditions.append(attr.in_(value[1]))
                        elif value[0] == "between" and len(value[1]) == 2:
                            conditions.append(attr.between(value[1][0], value[1][1]))
                        elif value[0] == "month":
                            conditions.append(func.date_format(attr, "%Y-%m") == value[1])
                        elif value[0] == "!=":
                            conditions.append(attr != value[1])
                        elif value[0] == ">":
                            conditions.append(attr > value[1])
                        elif value[0] == ">=":
                            conditions.append(attr >= value[1])
                        elif value[0] == "<=":
                            conditions.append(attr <= value[1])
                        else:
                            raise CustomException("SQL查询语法错误")
                else:
                    conditions.append(attr == value)
        return conditions
