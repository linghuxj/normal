import request from '@/axios'

export const getRecordOperationListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/admin/record/operations', params })
}
