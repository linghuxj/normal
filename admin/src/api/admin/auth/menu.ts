import request from '@/axios'

export const getMenuListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/admin/auth/menus', params })
}

export const delMenuListApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/admin/auth/menus', data })
}

export const addMenuListApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/admin/auth/menus', data })
}

export const putMenuListApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/admin/auth/menus/${data.id}`, data })
}

export const getMenuTreeOptionsApi = (): Promise<IResponse> => {
  return request.get({ url: '/admin/auth/menus/tree/options' })
}

export const getMenuRoleTreeOptionsApi = (): Promise<IResponse> => {
  return request.get({ url: '/admin/auth/menus/role/tree/options' })
}
