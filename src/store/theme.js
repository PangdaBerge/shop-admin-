import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  // 从 localStorage 恢复主题偏好，默认跟随系统
  const saved = localStorage.getItem('theme')
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
  const isDark = ref(saved ? saved === 'dark' : prefersDark)

  const toggle = () => {
    isDark.value = !isDark.value
  }

  // 监听变化：同步 DOM 类名 + 持久化到 localStorage
  watch(isDark, (val) => {
    localStorage.setItem('theme', val ? 'dark' : 'light')
    document.documentElement.classList.toggle('dark', val)
  }, { immediate: true })

  return { isDark, toggle }
})
