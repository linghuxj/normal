import request from '@/axios'
import type { Project, Dynamic, Team, RadarData, Shortcuts } from './types'

export const getProjectApi = (): Promise<IResponse<Project>> => {
  return request.get({ url: '/admin/workplace/project' })
}

export const getDynamicApi = (): Promise<IResponse<Dynamic[]>> => {
  return request.get({ url: '/admin/workplace/dynamic' })
}

export const getTeamApi = (): Promise<IResponse<Team[]>> => {
  return request.get({ url: '/admin/workplace/team' })
}

export const getRadarApi = (): Promise<IResponse<RadarData[]>> => {
  return request.get({ url: '/admin/workplace/radar' })
}

export const getShortcutsApi = (): Promise<IResponse<Shortcuts[]>> => {
  return request.get({ url: '/admin/workplace/shortcuts' })
}
