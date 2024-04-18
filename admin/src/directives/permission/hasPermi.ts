import type { App, Directive, DirectiveBinding } from 'vue'
import { useI18n } from '@/hooks/web/useI18n'
import { useUserStoreWithOut } from '@/store/modules/user'
import { isArray } from '@/utils/is'
import { intersection } from 'lodash-es'

const { t } = useI18n()

const userStore = useUserStoreWithOut()

// 全部权限
const all_permission = ['*.*.*']

const hasPermission = (value: string): boolean => {
  const permission = userStore.getPermissions
  if (!value) {
    throw new Error(t('permission.hasPermission'))
  }

  if (all_permission[0] === permission[0]) {
    return true
  }

  if (!isArray(value)) {
    return permission?.includes(value as string)
  }

  return (intersection(value, permission) as string[]).length > 0
}
function hasPermi(el: Element, binding: DirectiveBinding) {
  const value = binding.value

  const flag = hasPermission(value)
  if (!flag) {
    el.parentNode?.removeChild(el)
  }
}
const mounted = (el: Element, binding: DirectiveBinding<any>) => {
  hasPermi(el, binding)
}

const permiDirective: Directive = {
  mounted
}

export const setupPermissionDirective = (app: App<Element>) => {
  app.directive('hasPermi', permiDirective)
}

export default permiDirective
