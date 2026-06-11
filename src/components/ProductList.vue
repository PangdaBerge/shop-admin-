<template>
  <table class="w-full text-left border-collapse">
    <thead>
      <tr class="bg-blue-50 text-blue-800">
        <th class="p-3 border-b rounded-tl-lg">序号</th>
        <th class="p-3 border-b">商品名称</th>
        <th class="p-3 border-b">单价 (元)</th>
        <th class="p-3 border-b text-right rounded-tr-lg">操作</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(item, index) in data" :key="item.id" class="hover:bg-gray-50 border-b transition">
        
        <td class="p-3 text-gray-500 font-bold">{{ index + 1 }}</td>
        
        <td class="p-3 font-medium">{{ item.name }}</td>
        <td class="p-3 text-red-500 font-bold">¥{{ item.price }}</td>
        
        <td class="p-3 text-right">
          <button v-if="userStore.userInfo?.role === 'admin'" @click="$emit('remove', item.id)" class="text-red-500 hover:text-red-700 font-medium">下架</button>
          
          <button v-else @click="$emit('add-to-cart', item)" class="text-blue-500 hover:text-white hover:bg-blue-500 font-bold bg-blue-100 px-3 py-1 rounded transition duration-200">
            加入购物车
          </button>
        </td>
      </tr>
      
      <tr v-if="data.length === 0">
        <td colspan="4" class="p-8 text-center text-gray-400">
          <slot name="empty">暂无数据</slot>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script setup>
import { useUserStore } from '@/store/user'
const userStore = useUserStore()

defineProps({
  data: { type: Array, required: true }
})
defineEmits(['remove', 'add-to-cart'])
</script>