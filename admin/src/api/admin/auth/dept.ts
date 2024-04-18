import request from '@/axios'

export const getDeptListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/admin/auth/depts', params })
}

export const delDeptListApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/admin/auth/depts', data })
}

export const addDeptListApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/admin/auth/depts', data })
}

export const putDeptListApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/admin/auth/depts/${data.id}`, data })
}

export const getDeptTreeOptionsApi = (): Promise<IResponse> => {
  return request.get({ url: '/admin/auth/dept/tree/options' })
}

export const getDeptUserTreeOptionsApi = (): Promise<IResponse> => {
  return request.get({ url: '/admin/auth/dept/user/tree/options' })
}
