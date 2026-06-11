import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import axios from 'axios'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref(JSON.parse(localStorage.getItem('userInfo') || '{}'))

  watch(token, (newVal) => {
    if (newVal) localStorage.setItem('token', newVal)
    else localStorage.removeItem('token')
  })

  // 核心重构：向 Python 后端发送真实的登录请求
  const login = async (username, password) => {
    try {
      const res = await axios.post('http://localhost:3000/api/login', { username, password })
      if (res.data.code === 200) {
        token.value = res.data.data.token
        userInfo.value = res.data.data.user
        localStorage.setItem('userInfo', JSON.stringify(userInfo.value))
        return true
      } else {
        alert(res.data.message)
        return false
      }
    } catch (error) {
      alert('后端请求失败，请确保 Python 后端服务(3000端口)正在运行！')
      return false
    }
  }

  const logout = () => {
    token.value = ''
    userInfo.value = {}
    localStorage.removeItem('token')
    localStorage.removeItem('userInfo')
  }

  return { token, userInfo, login, logout }
})