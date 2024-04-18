from fastapi import Depends
from core.dependencies import Paging, QueryParams


class OperationParams(QueryParams):
    """
    列表分页
    """

    def __init__(
            self,
            summary: str = None,
            telephone: str = None,
            request_method: str = None,
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.summary = ("like", summary)
        self.telephone = ("like", telephone)
        self.request_method = request_method
        self.order = "desc"
