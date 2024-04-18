# 短信发送记录相关的模型


from pydantic import BaseModel, ConfigDict
from core.data_types import DatetimeStr


class SMSSendRecord(BaseModel):
    telephone: str
    status: bool = True
    user_id: int | None = None
    content: str | None = None
    desc: str | None = None
    scene: str | None = None


class SMSSendRecordSimpleOut(SMSSendRecord):
    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr

    model_config = ConfigDict(from_attributes=True)
