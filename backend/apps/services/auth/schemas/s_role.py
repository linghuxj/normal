# 角色模型

from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr
from .s_menu import MenuSimpleOut
from .s_dept import DeptSimpleOut


class Role(BaseModel):
    name: str
    disabled: bool = False
    order: int | None = None
    desc: str | None = None
    data_range: int = 4
    role_key: str
    is_admin: bool = False


class RoleSimpleOut(Role):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr


class RoleOut(RoleSimpleOut):
    model_config = ConfigDict(from_attributes=True)

    menus: list[MenuSimpleOut] = []
    depts: list[DeptSimpleOut] = []


class RoleIn(Role):
    menu_ids: list[int] = []
    dept_ids: list[int] = []


class RoleOptionsOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    label: str = Field(alias='name')
    value: int = Field(alias='id')
    disabled: bool
