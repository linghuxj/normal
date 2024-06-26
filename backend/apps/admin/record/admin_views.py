# API接口定义

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from utils.response import SuccessResponse
from apps.services.record import crud
from apps.services.auth.utils.current import AllUserAuth
from apps.services.auth.utils.validation.auth import Auth
from apps.services.record.params import LoginParams, OperationParams, SMSParams
from core.database import mongo_getter

app = APIRouter()


###########################################################
#    日志管理
###########################################################
@app.get("/logins", summary="获取登录日志列表")
async def get_record_login(p: LoginParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    datas, count = await crud.LoginRecordDal(auth.db).get_datas(**p.dict(), return_count=True)
    return SuccessResponse(datas, count=count)


@app.get("/operations", summary="获取操作日志列表")
async def get_record_operation(
        p: OperationParams = Depends(),
        db: AsyncIOMotorDatabase = Depends(mongo_getter),
        auth: Auth = Depends(AllUserAuth())
):
    count = await crud.OperationRecordDal(db).get_count(**p.to_count())
    datas = await crud.OperationRecordDal(db).get_datas(**p.dict())
    return SuccessResponse(datas, count=count)


@app.get("/sms/send/list", summary="获取短信发送列表")
async def get_sms_send_list(p: SMSParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    datas, count = await crud.SMSSendRecordDal(auth.db).get_datas(**p.dict(), return_count=True)
    return SuccessResponse(datas, count=count)


###########################################################
#    日志分析
###########################################################
@app.get("/analysis/user/login/distribute", summary="获取用户登录分布情况列表")
async def get_user_login_distribute(auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.LoginRecordDal(auth.db).get_user_distribute())
