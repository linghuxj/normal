import request from '@/axios'

/**
 * 图片资源管理管理
 */

export const getImagesListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/admin/resource/images', params })
}

export const addImagesApi = (data: any): Promise<IResponse> => {
  return request.post({
    url: '/admin/resource/images',
    headersType: 'multipart/form-data',
    data
  })
}

export const delImagesListApi = (data: number[]): Promise<IResponse> => {
  return request.delete({ url: `/admin/resource/images`, data })
}

export const getImagesApi = (dataId: number): Promise<IResponse> => {
  return request.get({ url: `/admin/resource/images/${dataId}` })
}
