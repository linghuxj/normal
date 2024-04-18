import { AxiosResponse, InternalAxiosRequestConfig } from './types'
import { ElMessage } from 'element-plus'
import qs from 'qs'
import { SUCCESS_CODE, TRANSFORM_REQUEST_DATA, UNATHORIZED_CODE } from '@/constants'
import { objToFormData } from '@/utils'
import { useAppStore } from '@/store/modules/app'
import { useStorage } from '@/hooks/web/useStorage'
import request from '@/axios'
import { AxiosError } from 'axios'
import { useUserStore } from '@/store/modules/user'

const { getStorage, setStorage } = useStorage()

const defaultRequestInterceptors = (config: InternalAxiosRequestConfig) => {
  const appStore = useAppStore()
  const token = getStorage(appStore.getToken)
  if (token !== '') {
    ;(config.headers as any)['Authorization'] = token
  }
  if (
    config.method === 'post' &&
    config.headers['Content-Type'] === 'application/x-www-form-urlencoded'
  ) {
    config.data = qs.stringify(config.data)
  } else if (
    TRANSFORM_REQUEST_DATA &&
    config.method === 'post' &&
    config.headers['Content-Type'] === 'multipart/form-data'
  ) {
    config.data = objToFormData(config.data)
  }
  if (config.method === 'get' && config.params) {
    let url = config.url as string
    url += '?'
    const keys = Object.keys(config.params)
    for (const key of keys) {
      if (config.params[key] !== void 0 && config.params[key] !== null) {
        url += `${key}=${encodeURIComponent(config.params[key])}&`
      }
    }
    url = url.substring(0, url.length - 1)
    config.params = {}
    config.url = url
  }
  return config
}

const defaultResponseInterceptors = (response: AxiosResponse) => {
  if (response?.config?.responseType === 'blob') {
    // 如果是文件流，直接过
    return response
  } else if (response.data.code === SUCCESS_CODE) {
    const refresh = response.headers['if-refresh']
    if (refresh === '1') {
      refreshToken().then((res) => {
        const appStore = useAppStore()
        setStorage(appStore.getToken, `${res.data.token_type} ${res.data.access_token}`)
        setStorage(appStore.getRefreshToken, res.data.refresh_token)
      })
    }
    return response.data
  } else if (response.data.code === UNATHORIZED_CODE) {
    // 因token无效，token过期导致
    refreshToken().then((res) => {
      const appStore = useAppStore()
      setStorage(appStore.getToken, `${res.data.token_type} ${res.data.access_token}`)
      setStorage(appStore.getRefreshToken, res.data.refresh_token)
      ElMessage.error('操作失败，请重试')
    })
  } else {
    ElMessage.error(response.data.message)
  }
}

const defaultResponseInterceptorsError = (error: AxiosError) => {
  console.log('err： ' + error) // for debug
  let message = error.message
  const userStore = useUserStore()
  const status = error.response?.status
  switch (status) {
    case 400:
      message = '请求错误'
      break
    case 401:
      // token过期
      userStore.logout()
      message = '登录过期，请重新登录'
      break
    case 403:
      // token过期
      userStore.logout()
      message = '无权限访问，请联系管理员'
      break
    case 404:
      message = `请求地址出错: ${error.response?.config.url}`
      break
    case 408:
      message = '请求超时'
      break
    case 500:
      message = '服务器内部错误'
      break
    case 501:
      message = '服务未实现'
      break
    case 502:
      message = '网关错误'
      break
    case 503:
      message = '服务不可用'
      break
    case 504:
      message = '网关超时'
      break
    case 505:
      message = 'HTTP版本不受支持'
      break
    default:
      break
  }
  ElMessage.error(message)
  return Promise.reject(error)
}

// 请求刷新Token
const refreshToken = (): Promise<IResponse> => {
  const appStore = useAppStore()
  const data = getStorage(appStore.getRefreshToken)
  return request.post({ url: '/auth/token/refresh', data })
}

export { defaultResponseInterceptors, defaultRequestInterceptors, defaultResponseInterceptorsError }
