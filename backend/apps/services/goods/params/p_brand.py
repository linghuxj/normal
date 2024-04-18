from fastapi import Depends, Query

from core.dependencies import QueryParams, Paging


class BrandParams(QueryParams):
    """
    列表分页
    """

    def __init__(
            self,
            name: str | None = Query(None, title="品牌名称"),
            status: int | None = Query(None, title="状态"),
            category_id: int | None = Query(None, title="分类ID"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.order = "desc"
        self.order_field = "create_datetime"
        self.status = status
        self.name = ("like", name)
        self.category_id = category_id
