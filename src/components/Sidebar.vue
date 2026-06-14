<template>
  <!-- 移动端遮罩层 -->
  <div
    v-if="mobileOpen"
    class="fixed inset-0 bg-black/50 z-40 lg:hidden"
    @click="mobileOpen = false"
  />

  <!-- 侧边栏 -->
  <aside
    :class="[
      'fixed lg:sticky top-0 left-0 z-50 h-screen flex flex-col transition-all duration-300',
      'bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700',
      mobileOpen ? 'w-64 translate-x-0' : 'w-64 -translate-x-full lg:translate-x-0 lg:w-64',
    ]"
  >
    <!-- Logo -->
    <div class="flex items-center justify-between h-16 px-4 border-b border-gray-200 dark:border-gray-700">
      <router-link to="/dashboard" class="flex items-center gap-2" @click="mobileOpen = false">
        <span class="text-2xl">🛒</span>
        <span class="font-bold text-gray-800 dark:text-white text-lg">商城后台</span>
      </router-link>
      <button
        class="lg:hidden text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-white"
        @click="mobileOpen = false"
      >
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>

    <!-- 导航菜单 -->
    <nav class="flex-1 overflow-y-auto py-4 px-3">
      <p class="px-3 mb-2 text-xs font-semibold text-gray-400 dark:text-gray-500 uppercase tracking-wider">主菜单</p>

      <router-link
        v-for="item in menuItems"
        :key="item.path"
        :to="item.path"
        class="flex items-center gap-3 px-3 py-2.5 mb-1 rounded-lg text-sm font-medium transition-colors"
        :class="isActive(item.path)
          ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400'
          : 'text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'"
        @click="mobileOpen = false"
      >
        <span class="text-lg">{{ item.icon }}</span>
        <span>{{ item.label }}</span>
        <span v-if="item.badge" class="ml-auto bg-red-500 text-white text-xs px-1.5 py-0.5 rounded-full">{{ item.badge }}</span>
      </router-link>
    </nav>

    <!-- 底部用户区 -->
    <div class="p-4 border-t border-gray-200 dark:border-gray-700">
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white text-sm font-bold">
          {{ userStore.userInfo?.name?.charAt(0)?.toUpperCase() || 'U' }}
        </div>
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium text-gray-700 dark:text-gray-200 truncate">{{ userStore.userInfo?.name }}</p>
          <p class="text-xs text-gray-400 dark:text-gray-500">{{ userStore.userInfo?.role === 'admin' ? '管理员' : '普通用户' }}</p>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'

const route = useRoute()
const userStore = useUserStore()
const emit = defineEmits(['update:mobileOpen'])
const props = defineProps({ mobileOpen: { type: Boolean, default: false } })

const mobileOpen = computed({
  get: () => props.mobileOpen,
  set: (val) => emit('update:mobileOpen', val),
})

const isActive = (path) => route.path === path

const menuItems = [
  { path: '/dashboard', icon: '📊', label: '控制台' },
  { path: '/taskboard', icon: '📋', label: '任务看板' },
]
</script>
