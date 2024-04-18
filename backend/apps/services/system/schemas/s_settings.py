# 系统配置模型

from pydantic import BaseModel, ConfigDict
from core.data_types import DatetimeStr


class Settings(BaseModel):
    config_label: str | None = None
    config_key: str
    config_value: str | None = None
    remark: str | None = None
    disabled: bool | None = None
    tab_id: int


class SettingsSimpleOut(Settings):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr


class SettingsTab(BaseModel):
    title: str
    classify: str
    tab_label: str
    tab_name: str
    hidden: bool


class SettingsTabSimpleOut(SettingsTab):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr
