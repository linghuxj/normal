import request from '@/axios'
import type { UserLoginType } from './types'

export const loginApi = (data: UserLoginType): Promise<IResponse> => {
  return request.post({ url: '/auth/login', data })
}

export const getRoleMenusApi = (): Promise<IResponse<AppCustomRouteRecordRaw[]>> => {
  return request.get({ url: '/auth/getMenuList' })
}

export const postSMSCodeApi = (params: any): Promise<IResponse> => {
  return request.post({ url: '/admin/system/sms/send', params })
}
