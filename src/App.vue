<template>
  <!-- 登录页不使用侧边栏布局 -->
  <div v-if="$route.path === '/login'" class="min-h-screen bg-gray-100 dark:bg-gray-900 transition-colors">
    <router-view />
  </div>

  <!-- 主布局：侧边栏 + 内容区 -->
  <div v-else class="flex h-screen overflow-hidden bg-gray-50 dark:bg-gray-950 transition-colors">
    <Sidebar v-model:mobileOpen="mobileOpen" />
    <main class="flex-1 overflow-y-auto">
      <!-- 移动端顶栏 -->
      <header class="sticky top-0 z-30 lg:hidden flex items-center justify-between h-14 px-4 bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700">
        <button
          class="p-1.5 rounded-lg text-gray-500 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-800"
          @click="mobileOpen = true"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
        <span class="font-bold text-gray-800 dark:text-white">商城后台</span>
        <ThemeToggle />
      </header>

      <!-- 桌面端顶栏 -->
      <header class="hidden lg:flex items-center justify-end h-14 px-6 bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700">
        <ThemeToggle />
      </header>

      <div class="p-4 md:p-6 lg:p-8">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Sidebar from '@/components/Sidebar.vue'
import ThemeToggle from '@/components/ThemeToggle.vue'

const mobileOpen = ref(false)
</script>