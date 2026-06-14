<template>
  <table class="w-full text-left border-collapse">
    <thead>
      <tr class="bg-blue-50 dark:bg-blue-900/30 text-blue-800 dark:text-blue-300 text-sm">
        <th class="p-3 rounded-tl-lg">序号</th>
        <th class="p-3">商品名称</th>
        <th class="p-3 hidden sm:table-cell">分类</th>
        <th class="p-3">单价</th>
        <th class="p-3 text-right rounded-tr-lg">操作</th>
      </tr>
    </thead>
    <tbody class="divide-y divide-gray-100 dark:divide-gray-700">
      <tr v-for="(item, index) in data" :key="item.id" class="hover:bg-gray-50 dark:hover:bg-gray-700/30 transition-colors text-sm">
        <td class="p-3 text-gray-400 dark:text-gray-500 font-mono">{{ index + 1 }}</td>
        <td class="p-3 font-medium text-gray-700 dark:text-gray-200">{{ item.name }}</td>
        <td class="p-3 hidden sm:table-cell">
          <span class="px-2 py-0.5 rounded-full text-xs font-medium bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400">
            {{ item.category || '未分类' }}
          </span>
        </td>
        <td class="p-3 text-red-500 dark:text-red-400 font-bold">¥{{ item.price }}</td>
        <td class="p-3 text-right">
          <button
            v-if="userStore.userInfo?.role === 'admin'"
            @click="$emit('remove', item.id)"
            class="text-red-500 hover:text-red-700 dark:hover:text-red-300 font-medium text-sm"
          >
            下架
          </button>
          <button
            v-else
            @click="$emit('add-to-cart', item)"
            class="text-blue-500 hover:text-white hover:bg-blue-500 dark:hover:bg-blue-600 font-bold bg-blue-50 dark:bg-blue-900/30 px-3 py-1.5 rounded-lg transition duration-200 text-sm"
          >
            加入购物车
          </button>
        </td>
      </tr>

      <tr v-if="data.length === 0">
        <td colspan="5" class="p-8 text-center text-gray-400 dark:text-gray-500">
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
