from fastapi import Depends
from core.dependencies import Paging, QueryParams


class DictDetailParams(QueryParams):
    """
    列表分页
    """

    def __init__(self, dict_type_id: int = None, label: str = None, params: Paging = Depends()):
        super().__init__(params)
        self.dict_type_id = dict_type_id
        self.label = ("like", label)


class DictTypeParams(QueryParams):
    """
    列表分页
    """

    def __init__(self, dict_name: str = None, dict_type: str = None, params: Paging = Depends()):
        super().__init__(params)
        self.dict_name = ("like", dict_name)
        self.dict_type = ("like", dict_type)
