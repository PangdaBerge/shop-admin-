import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/store/user'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { title: '登录 - 商城后台管理系统' }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue'),
    // requiresAuth 标记该页面需要登录权限才能访问
    meta: { title: '控制台 - 商城后台管理系统', requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 第四阶段核心：全局路由权限守卫 (Login Guard)
router.beforeEach((to, from, next) => {
  // 动态修改网页标签页的标题
  if (to.meta.title) {
    document.title = to.meta.title
  }

  const userStore = useUserStore()

  // 验证逻辑：
  // 1. 如果去往需要权限的页面，但没有凭证(token)，强制重定向到登录页
  if (to.meta.requiresAuth && !userStore.token) {
    next('/login')
  } 
  // 2. 如果已经登录了，还想回登录页，直接拦截并送回控制台
  else if (to.path === '/login' && userStore.token) {
    next('/dashboard')
  } 
  // 3. 其他情况正常放行
  else {
    next()
  }
})

export default router