import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import AutoImport from 'unplugin-auto-import/vite'

export default defineConfig({
  plugins: [
    vue(),
    // 配置自动导入插件
    AutoImport({
      imports: ['vue', 'vue-router', 'pinia'], 
      dts: false
    })
  ],
  resolve: {
    // 配置路径别名 @
    alias: {
      '@': path.resolve(__dirname, 'src')
    }
  }
})