import request from '@/axios'

export const getBrandListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/admin/goods/brands', params })
}

export const addBrandApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/admin/goods/brands', data })
}

export const delBrandApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/admin/goods/brands', data })
}

export const putBrandApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/admin/goods/brands/${data.id}`, data })
}

export const getBrandApi = (dataId: number): Promise<IResponse> => {
  return request.get({ url: `/admin/goods/brands/${dataId}` })
}
