<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100 dark:bg-gray-900 transition-colors px-4">
    <!-- 深色模式切换 -->
    <div class="absolute top-4 right-4">
      <ThemeToggle />
    </div>

    <div class="bg-white dark:bg-gray-800 p-8 rounded-xl shadow-lg dark:shadow-gray-900/50 w-full max-w-md transition-colors">
      <div class="text-center mb-8">
        <span class="text-5xl">🛒</span>
        <h2 class="text-2xl font-bold mt-3 text-gray-800 dark:text-white">商城后台管理系统</h2>
        <p class="text-sm text-gray-400 dark:text-gray-500 mt-1">请登录您的账户</p>
      </div>

      <form @submit.prevent="handleLogin">
        <div class="mb-4">
          <label class="block text-gray-700 dark:text-gray-300 text-sm font-bold mb-2">用户名</label>
          <input
            v-model="username"
            type="text"
            class="w-full px-3 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
            placeholder="管理员 admin，普通用户 zff"
            required
          >
        </div>

        <div class="mb-6">
          <label class="block text-gray-700 dark:text-gray-300 text-sm font-bold mb-2">密码</label>
          <input
            v-model="password"
            type="password"
            class="w-full px-3 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
            placeholder="请输入密码 123456"
            required
          >
        </div>

        <button
          type="submit"
          class="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2.5 px-4 rounded-lg transition duration-200 transform active:scale-95"
        >
          登 录
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import ThemeToggle from '@/components/ThemeToggle.vue'

const username = ref('')
const password = ref('')

const userStore = useUserStore()
const router = useRouter()

const handleLogin = async () => {
  const success = await userStore.login(username.value, password.value)
  if (success) {
    router.push('/dashboard')
  }
}
</script>