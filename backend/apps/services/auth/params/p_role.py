from fastapi import Depends, Query
from core.dependencies import Paging, QueryParams


class RoleParams(QueryParams):
    """
    列表分页
    """

    def __init__(
            self,
            name: str | None = Query(None, title="角色名称"),
            role_key: str | None = Query(None, title="权限字符"),
            disabled: bool | None = Query(None, title="是否禁用"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.name = ("like", name)
        self.role_key = ("like", role_key)
        self.disabled = disabled
