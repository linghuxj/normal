import request from '@/axios'

export const getUserListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/admin/auth/users', params })
}

export const addUserListApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/admin/auth/users', data })
}

export const delUserListApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/admin/auth/users', data })
}

export const putUserListApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/admin/auth/users/${data.id}`, data })
}

export const getUserApi = (dataId: number): Promise<IResponse> => {
  return request.get({ url: `/admin/auth/users/${dataId}` })
}

export const postCurrentUserResetPassword = (data: any): Promise<IResponse> => {
  return request.post({ url: `/admin/auth/user/current/reset/password`, data })
}

export const postCurrentUserUpdateInfo = (data: any): Promise<IResponse> => {
  return request.post({ url: `/admin/auth/user/current/update/info`, data })
}

export const getCurrentAdminUserInfo = (): Promise<IResponse> => {
  return request.get({ url: `/admin/auth/user/admin/current/info` })
}

export const postExportUserQueryListApi = (params: any, data: any): Promise<IResponse> => {
  return request.post({ url: `/admin/auth/user/export/query/list/to/excel`, params, data })
}

export const getImportTemplateApi = (): Promise<IResponse> => {
  return request.get({ url: `/admin/auth/user/download/import/template` })
}

export const postImportUserApi = (data: any): Promise<IResponse> => {
  return request.post({
    url: `/admin/auth/import/users`,
    headers: {
      'Content-Type': 'multipart/form-data'
    },
    data
  })
}

export const postUsersInitPasswordSendSMSApi = (data: any): Promise<IResponse> => {
  return request.post({ url: `/admin/auth/users/init/password/send/sms`, data })
}

export const postUsersInitPasswordSendEmailApi = (data: any): Promise<IResponse> => {
  return request.post({ url: `/admin/auth/users/init/password/send/email`, data })
}
