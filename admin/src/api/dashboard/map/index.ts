import request from '@/axios'

export const getUserLoginDistributeApi = (): Promise<IResponse> => {
  return request.get({ url: '/admin/record/analysis/user/login/distribute' })
}
