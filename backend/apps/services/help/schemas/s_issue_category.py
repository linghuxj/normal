# 常见问题类别


from pydantic import BaseModel, Field, ConfigDict
from core.data_types import DatetimeStr
from apps.services.auth.schemas import UserSimpleOut


class IssueCategory(BaseModel):
    name: str | None = None
    platform: str | None = None
    is_active: bool | None = None

    create_user_id: int | None = None


class IssueCategorySimpleOut(IssueCategory):
    model_config = ConfigDict(from_attributes=True)

    id: int
    update_datetime: DatetimeStr
    create_datetime: DatetimeStr


class IssueCategoryListOut(IssueCategorySimpleOut):
    model_config = ConfigDict(from_attributes=True)

    create_user: UserSimpleOut


class IssueCategoryOptionsOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    label: str = Field(alias='name')
    value: int = Field(alias='id')
