import request from '@/axios'

export const getCateListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/admin/goods/categories', params })
}

export const addCategoryApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/admin/goods/categories', data })
}

export const delCategoryApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/admin/goods/categories', data })
}

export const putCategoryApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/admin/goods/categories/${data.id}`, data })
}

export const getCategoryApi = (dataId: number): Promise<IResponse> => {
  return request.get({ url: `/admin/goods/categories/${dataId}` })
}
