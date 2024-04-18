import request from '@/axios'

export const getTaskListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/admin/system/tasks', params })
}

export const addTaskListApi = (data: any): Promise<IResponse> => {
  return request.post({ url: '/admin/system/tasks', data })
}

export const delTaskListApi = (dataId: string): Promise<IResponse> => {
  return request.delete({ url: `/admin/system/tasks?_id=${dataId}` })
}

export const putTaskListApi = (dataId: string, data: any): Promise<IResponse> => {
  return request.put({ url: `/admin/system/tasks?_id=${dataId}`, data })
}

export const getTaskApi = (dataId: string): Promise<IResponse> => {
  return request.get({ url: `/admin/system/task?_id=${dataId}` })
}

export const getTaskGroupOptionsApi = (): Promise<IResponse> => {
  return request.get({ url: '/admin/system/task/group/options' })
}

export const getTaskRecordListApi = (params: any): Promise<IResponse> => {
  return request.get({ url: '/admin/system/task/records', params })
}

export const runOnceTaskApi = (dataId: string): Promise<IResponse> => {
  return request.post({ url: `/admin/system/task?_id=${dataId}` })
}
