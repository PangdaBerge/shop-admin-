import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import './style.css' // 引入全局样式（包含 Tailwind）
import App from './App.vue'

const app = createApp(App)

// 挂载 Pinia 和 Router
app.use(createPinia())
app.use(router)

app.mount('#app')