from fastapi import Depends
from core.dependencies import Paging, QueryParams


class LoginParams(QueryParams):
    """
    列表分页
    """

    def __init__(
            self,
            ip: str = None,
            address: str = None,
            telephone: str = None,
            status: bool = None,
            platform: str = None,
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.ip = ("like", ip)
        self.telephone = ("like", telephone)
        self.address = ("like", address)
        self.status = status
        self.platform = platform
