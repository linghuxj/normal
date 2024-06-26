import request from '@/axios'

export const getDictTypeListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/admin/system/dict/types', params })
}

export const addDictTypeListApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/admin/system/dict/types', data })
}

export const delDictTypeListApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/admin/system/dict/types', data })
}

export const putDictTypeListApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/admin/system/dict/types/${data.id}`, data })
}

export const getDictTypeApi = (dataId: number): Promise<IResponse> => {
  return request.get({ url: `/admin/system/dict/types/${dataId}` })
}

export const getDictTypeOptionsApi = (): Promise<IResponse> => {
  return request.get({ url: `/admin/system/dict/types/options` })
}

export const getDictTypeDetailsApi = (data: any): Promise<IResponse> => {
  return request.post({ url: `/admin/system/dict/types/details`, data })
}

export const getDictDetailsListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/admin/system/dict/details', params })
}

export const addDictDetailsListApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/admin/system/dict/details', data })
}

export const delDictDetailsListApi = (data: any): Promise<IResponse> => {
  return request.delete({ url: '/admin/system/dict/details', data })
}

export const putDictDetailsListApi = (data: any): Promise<IResponse> => {
  return request.put({ url: `/admin/system/dict/details/${data.id}`, data })
}

export const getDictDetailsApi = (dataId: number): Promise<IResponse> => {
  return request.get({ url: `/admin/system/dict/details/${dataId}` })
}
