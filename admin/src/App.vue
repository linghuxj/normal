<script setup lang="ts">
import { computed } from 'vue'
import { useAppStore } from '@/store/modules/app'
import { ConfigGlobal } from '@/components/ConfigGlobal'
import { useDesign } from '@/hooks/web/useDesign'
import { useStorage } from '@/hooks/web/useStorage'
import { getSystemBaseConfigApi } from '@/api/admin/system/settings'
import { isDark } from '@/utils/is'

const { getPrefixCls } = useDesign()

const prefixCls = getPrefixCls('app')

const appStore = useAppStore()

const currentSize = computed(() => appStore.getCurrentSize)

const greyMode = computed(() => appStore.getGreyMode)

const { getStorage } = useStorage()

const setDefaultTheme = () => {
  if (getStorage('isDark') !== null) {
    appStore.setIsDark(getStorage('isDark'))
    return
  } else {
    appStore.initTheme()
  }
  const isDarkTheme = isDark()
  appStore.setIsDark(isDarkTheme)
}

// 添加mate标签
const addMeta = (name: string, content: string) => {
  const meta = document.createElement('meta')
  meta.content = content
  meta.name = name
  document.getElementsByTagName('head')[0].appendChild(meta)
}

// 获取并设置系统配置
const setSystemConfig = async () => {
  const res = await getSystemBaseConfigApi()
  if (res) {
    appStore.setTitle(res.data.web_title || import.meta.env.VITE_APP_TITLE)
    appStore.setLogoImage(res.data.web_logo || '/media/system/logo.png')
    appStore.setFooterContent(res.data.web_copyright || 'Copyright ©2021-present Smtro')
    appStore.setIcpNumber(res.data.web_icp_number || '')
    addMeta('description', res.data.web_desc || '通用型后台管理系统')
  }
}

setDefaultTheme()
setSystemConfig()
</script>

<template>
  <ConfigGlobal :size="currentSize">
    <RouterView :class="greyMode ? `${prefixCls}-grey-mode` : ''" />
  </ConfigGlobal>
</template>

<style lang="less">
@prefix-cls: ~'@{namespace}-app';

.size {
  width: 100%;
  height: 100%;
}

html,
body {
  padding: 0 !important;
  margin: 0;
  overflow: hidden;
  .size;

  #app {
    .size;
  }
}

.@{prefix-cls}-grey-mode {
  filter: grayscale(100%);
}
</style>
