from fastapi import Depends
from core.dependencies import Paging, QueryParams


class ImagesParams(QueryParams):
    """
    列表分页
    """

    def __init__(
            self,
            filename: str = None,
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.filename = ('like', filename)
        self.order = "desc"
        self.order_field = "create_datetime"
