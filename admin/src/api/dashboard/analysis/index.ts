import request from '@/axios'
import type { UserAccessSource, WeeklyUserActivity, MonthlySales } from './types'

export const getRandomNumberApi = (): Promise<IResponse<any>> => {
  return request.get({ url: '/admin/analysis/random/number' })
}

export const getUserAccessSourceApi = (): Promise<IResponse<UserAccessSource[]>> => {
  return request.get({ url: '/admin/analysis/user/access/source' })
}

export const getWeeklyUserActivityApi = (): Promise<IResponse<WeeklyUserActivity[]>> => {
  return request.get({ url: '/admin/analysis/weekly/user/activity' })
}

export const getMonthlySalesApi = (): Promise<IResponse<MonthlySales[]>> => {
  return request.get({ url: '/admin/analysis/monthly/sales' })
}
