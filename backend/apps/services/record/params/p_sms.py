from fastapi import Depends
from core.dependencies import Paging, QueryParams


class SMSParams(QueryParams):
    """
    列表分页
    """

    def __init__(self, telephone: str = None, params: Paging = Depends()):
        super().__init__(params)
        self.telephone = ("like", telephone)
