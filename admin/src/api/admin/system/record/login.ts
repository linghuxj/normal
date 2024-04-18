import request from '@/axios'

export const getRecordLoginListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/admin/record/logins', params })
}
