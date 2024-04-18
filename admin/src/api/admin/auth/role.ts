import request from '@/axios'

export const getRoleListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/admin/auth/roles', params })
}

export const addRoleListApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/admin/auth/roles', data })
}

export const delRoleListApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/admin/auth/roles', data })
}

export const putRoleListApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/admin/auth/roles/${data.id}`, data })
}

export const getRoleApi = (dataId: number): Promise<IResponse> => {
  return request.get({ url: `/admin/auth/roles/${dataId}` })
}

export const getRoleOptionsApi = (): Promise<IResponse> => {
  return request.get({ url: `/admin/auth/roles/options` })
}
