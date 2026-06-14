<template>
  <div class="space-y-6">
    <!-- ===== 顶部工具栏：搜索 + 分类 + 上架 ===== -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-4 md:p-6 transition-colors">
      <!-- 第一行：标题 + 用户信息 + 退出 -->
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 mb-4 pb-4 border-b border-gray-100 dark:border-gray-700">
        <div>
          <h1 class="text-xl md:text-2xl font-bold text-gray-800 dark:text-white">🛍️ 商品管理</h1>
          <p class="text-xs md:text-sm text-gray-400 dark:text-gray-500 mt-1">
            当前用户: <strong class="text-blue-600 dark:text-blue-400">{{ userStore.userInfo?.name }}</strong>
            (<span :class="userStore.userInfo?.role === 'admin' ? 'text-purple-600 dark:text-purple-400' : 'text-green-600 dark:text-green-400'">{{ userStore.userInfo?.role === 'admin' ? '系统管理员' : '普通用户' }}</span>)
          </p>
        </div>
        <button @click="handleLogout" class="text-sm bg-gray-100 dark:bg-gray-700 hover:bg-red-500 dark:hover:bg-red-500 hover:text-white text-gray-600 dark:text-gray-300 px-4 py-2 rounded-lg transition duration-200">
          安全退出
        </button>
      </div>

      <!-- 第二行：搜索框 + 分类筛选 -->
      <div class="flex flex-col md:flex-row gap-3 items-start md:items-end">
        <div class="w-full md:w-64">
          <label class="block text-xs font-semibold text-gray-500 dark:text-gray-400 mb-1">🔍 搜索商品</label>
          <input
            v-model="searchKey"
            type="text"
            placeholder="输入名称搜索..."
            class="w-full px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm transition-colors"
          >
        </div>

        <div class="w-full md:w-auto">
          <label class="block text-xs font-semibold text-gray-500 dark:text-gray-400 mb-1">📂 分类筛选</label>
          <select
            v-model="selectedCategory"
            class="w-full md:w-auto px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm transition-colors"
          >
            <option value="全部">全部</option>
            <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
          </select>
        </div>

        <!-- 管理员上架区 -->
        <div v-if="userStore.userInfo?.role === 'admin'" class="flex flex-wrap gap-2 w-full md:w-auto">
          <input v-model="newItemName" type="text" placeholder="商品名称" class="flex-1 md:flex-none px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm transition-colors min-w-[120px]">
          <input v-model="newItemPrice" type="number" placeholder="价格" class="w-20 px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm transition-colors">
          <select v-model="newItemCategory" class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm transition-colors">
            <option value="">选择分类</option>
            <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
            <option value="__new__">+ 新建分类</option>
          </select>
          <input v-if="newItemCategory === '__new__'" v-model="customCategory" type="text" placeholder="输入新分类名" class="w-32 px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm transition-colors">
          <button @click="addProduct" class="bg-green-500 hover:bg-green-600 text-white font-bold px-4 py-2 rounded-lg transition duration-200 whitespace-nowrap text-sm">
            + 上架
          </button>
        </div>
      </div>
    </div>

    <!-- ===== 主内容区：商品列表 + 购物车 ===== -->
    <div class="flex flex-col lg:flex-row gap-6">
      <!-- 商品列表 -->
      <div :class="userStore.userInfo?.role === 'user' ? 'lg:w-2/3' : 'w-full'">
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-4 md:p-6 transition-colors">
          <h2 class="text-lg font-bold text-gray-800 dark:text-white mb-4">
            🛍️ 商品列表
            <span class="text-sm text-gray-400 dark:text-gray-500 font-normal ml-2">{{ filteredProducts.length }} 件商品</span>
          </h2>
          <ProductList :data="filteredProducts" @remove="deleteProduct" @add-to-cart="cartStore.addToCart">
            <template #empty>
              <span v-if="searchKey || selectedCategory !== '全部'">没有找到匹配的商品 ~</span>
              <span v-else>数据加载中...</span>
            </template>
          </ProductList>
        </div>
      </div>

      <!-- 购物车 (仅普通用户) -->
      <div v-if="userStore.userInfo?.role === 'user'" class="lg:w-1/3">
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-4 md:p-6 sticky top-4 transition-colors">
          <h2 class="text-lg font-bold text-gray-800 dark:text-white mb-4">🛒 我的购物车</h2>
          <div v-if="cartStore.items.length === 0" class="text-gray-400 dark:text-gray-500 text-center py-10">
            购物车空空如也，快去选购吧！
          </div>
          <div v-else class="space-y-3">
            <div v-for="item in cartStore.items" :key="item.id" class="flex justify-between items-center bg-gray-50 dark:bg-gray-700/50 p-3 rounded-lg transition-colors">
              <div class="min-w-0 flex-1">
                <div class="font-medium text-gray-700 dark:text-gray-200 text-sm truncate">{{ item.name }}</div>
                <div class="text-red-500 dark:text-red-400 font-medium text-xs mt-0.5">
                  ¥{{ item.price }}
                  <span class="text-gray-400 dark:text-gray-500 ml-1">x {{ item.quantity }}</span>
                </div>
              </div>
              <button @click="cartStore.removeFromCart(item.id)" class="text-red-400 hover:text-red-600 dark:hover:text-red-300 text-sm ml-3 shrink-0">移除</button>
            </div>
            <div class="pt-4 border-t-2 border-dashed border-gray-200 dark:border-gray-600">
              <div class="flex justify-between items-center font-bold text-lg mb-4">
                <span class="text-gray-700 dark:text-gray-300">总计</span>
                <span class="text-red-500 dark:text-red-400 text-2xl">¥{{ cartStore.totalPrice }}</span>
              </div>
              <button @click="checkout" class="w-full bg-red-500 hover:bg-red-600 text-white font-bold py-3 rounded-lg shadow-md transition transform active:scale-95">
                立即结算付款
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ===== 订单表格 ===== -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-4 md:p-6 transition-colors">
      <h2 class="text-lg font-bold text-gray-800 dark:text-white mb-4">
        🧾 {{ userStore.userInfo?.role === 'admin' ? '全站订单监控' : '我的历史订单' }}
      </h2>
      <!-- 桌面端表格 -->
      <div class="hidden md:block overflow-x-auto">
        <table class="w-full text-left">
          <thead>
            <tr class="bg-gray-100 dark:bg-gray-700/50 text-gray-600 dark:text-gray-300 text-sm">
              <th class="p-3 rounded-tl-lg">订单号</th>
              <th class="p-3">购买用户</th>
              <th class="p-3">购买明细</th>
              <th class="p-3">支付总额</th>
              <th class="p-3 rounded-tr-lg">交易时间</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100 dark:divide-gray-700">
            <tr v-for="order in orders" :key="order.id" class="hover:bg-gray-50 dark:hover:bg-gray-700/30 transition-colors text-sm">
              <td class="p-3 text-gray-400 dark:text-gray-500">#{{ order.id }}</td>
              <td class="p-3 font-bold text-blue-600 dark:text-blue-400">{{ order.username }}</td>
              <td class="p-3 text-gray-600 dark:text-gray-400">{{ order.items_detail }}</td>
              <td class="p-3 font-bold text-red-500 dark:text-red-400">¥{{ order.total_price }}</td>
              <td class="p-3 text-gray-400 dark:text-gray-500 text-xs">{{ order.created_at }}</td>
            </tr>
            <tr v-if="orders.length === 0">
              <td colspan="5" class="p-8 text-center text-gray-400 dark:text-gray-500">目前还没有任何订单数据哦~</td>
            </tr>
          </tbody>
        </table>
      </div>
      <!-- 移动端卡片 -->
      <div class="md:hidden space-y-3">
        <div v-for="order in orders" :key="order.id" class="bg-gray-50 dark:bg-gray-700/30 p-4 rounded-lg">
          <div class="flex justify-between items-start mb-2">
            <span class="text-gray-400 text-xs">#{{ order.id }}</span>
            <span class="text-red-500 font-bold">¥{{ order.total_price }}</span>
          </div>
          <div class="text-sm text-gray-600 dark:text-gray-400 mb-1">{{ order.items_detail }}</div>
          <div class="flex justify-between text-xs text-gray-400">
            <span class="text-blue-600 dark:text-blue-400">{{ order.username }}</span>
            <span>{{ order.created_at }}</span>
          </div>
        </div>
        <div v-if="orders.length === 0" class="text-center text-gray-400 dark:text-gray-500 py-8">暂无订单</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { useCartStore } from '@/store/cart'
import ProductList from '@/components/ProductList.vue'
import axios from 'axios'

const userStore = useUserStore()
const cartStore = useCartStore()
const router = useRouter()

const products = ref([])
const orders = ref([])
const categories = ref([])
const searchKey = ref('')
const selectedCategory = ref('全部')
const newItemName = ref('')
const newItemPrice = ref('')
const newItemCategory = ref('')
const customCategory = ref('')

const API = 'http://localhost:3000/api'

const fetchProducts = async () => {
  try {
    const params = selectedCategory.value !== '全部' ? { category: selectedCategory.value } : {}
    const res = await axios.get(`${API}/products`, { params })
    if (res.data.code === 200) products.value = res.data.data
  } catch (e) { console.error('获取商品失败', e) }
}

const fetchCategories = async () => {
  try {
    const res = await axios.get(`${API}/categories`)
    if (res.data.code === 200) categories.value = res.data.data
  } catch (e) { console.error('获取分类失败', e) }
}

const fetchOrders = async () => {
  try {
    const res = await axios.get(`${API}/orders`, { headers: { Authorization: userStore.token } })
    if (res.data.code === 200) orders.value = res.data.data
  } catch (e) { console.error('获取订单失败', e) }
}

onMounted(() => {
  fetchProducts()
  fetchCategories()
  fetchOrders()
})

// 分类切换时重新获取
watch(selectedCategory, () => fetchProducts())

const filteredProducts = computed(() => {
  if (!searchKey.value) return products.value
  return products.value.filter(p => p.name.toLowerCase().includes(searchKey.value.toLowerCase()))
})

const addProduct = async () => {
  if (!newItemName.value || !newItemPrice.value) return alert('请填写完整信息')
  const category = newItemCategory.value === '__new__'
    ? (customCategory.value || '未分类')
    : (newItemCategory.value || '未分类')

  try {
    await axios.post(`${API}/products`, {
      name: newItemName.value,
      price: Number(newItemPrice.value),
      category
    }, { headers: { Authorization: userStore.token } })
    newItemName.value = ''
    newItemPrice.value = ''
    newItemCategory.value = ''
    customCategory.value = ''
    fetchProducts()
    fetchCategories()
  } catch (e) { alert('上架失败，可能权限不足') }
}

const deleteProduct = async (id) => {
  try {
    await axios.delete(`${API}/products/${id}`, { headers: { Authorization: userStore.token } })
    fetchProducts()
    fetchCategories()
  } catch (e) { alert('下架失败') }
}

const checkout = async () => {
  if (cartStore.items.length === 0) return alert('购物车是空的！')
  const details = cartStore.items.map(item => `${item.name} x${item.quantity}`).join(' | ')
  try {
    const res = await axios.post(`${API}/orders`, {
      total_price: cartStore.totalPrice,
      items_detail: details
    }, { headers: { Authorization: userStore.token } })
    if (res.data.code === 200) {
      alert(res.data.message)
      cartStore.clearCart()
      fetchOrders()
    }
  } catch (e) { alert('支付失败，请检查网络！') }
}

const handleLogout = () => {
  userStore.logout()
  cartStore.clearCart()
  router.push('/login')
}
</script>
