<template>
  <div class="min-h-screen bg-gray-50 p-8">
    <div class="max-w-7xl mx-auto bg-white p-6 rounded-lg shadow-sm">
      
      <div class="flex justify-between items-center border-b pb-4 mb-6">
        <h1 class="text-3xl font-bold text-gray-800">
          商城系统主控制台 <span class="text-sm text-gray-400 font-normal ml-2">v5.0 (终极版：真实支付)</span>
        </h1>
        <div class="flex items-center gap-4">
          <span class="text-sm text-gray-500">
            当前用户: <strong class="text-blue-600">{{ userStore.userInfo?.name }}</strong> 
            (<span class="text-xs text-purple-600 font-bold">{{ userStore.userInfo?.role === 'admin' ? '系统管理员' : '普通用户' }}</span>)
          </span>
          <button @click="handleLogout" class="bg-gray-200 hover:bg-red-500 hover:text-white text-gray-600 px-4 py-2 rounded transition duration-200">
            安全退出
          </button>
        </div>
      </div>

      <div class="mb-6 flex justify-between items-end bg-gray-100 p-4 rounded">
        <div class="w-1/3">
          <label class="block text-sm font-bold text-gray-700 mb-1">搜索商品</label>
          <input v-model="searchKey" type="text" placeholder="输入名称过滤..." class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
        </div>
        <div v-if="userStore.userInfo?.role === 'admin'" class="flex gap-2">
          <input v-model="newItemName" type="text" placeholder="新商品名称" class="px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
          <input v-model="newItemPrice" type="number" placeholder="价格" class="w-24 px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
          <button @click="addProduct" class="bg-green-500 hover:bg-green-600 text-white font-bold px-4 py-2 rounded">上架商品</button>
        </div>
      </div>

      <div class="flex gap-8 items-start mb-12">
        <div :class="userStore.userInfo?.role === 'user' ? 'w-2/3' : 'w-full'">
          <h2 class="text-xl font-bold border-b pb-3 mb-4 text-gray-800">🛍️ 商品列表</h2>
          <ProductList :data="filteredProducts" @remove="deleteProduct" @add-to-cart="cartStore.addToCart">
            <template #empty><span v-if="searchKey">没搜到相关商品~</span><span v-else>数据加载中...</span></template>
          </ProductList>
        </div>

        <div v-if="userStore.userInfo?.role === 'user'" class="w-1/3 bg-gray-50 border rounded-lg p-5 shadow-inner sticky top-8">
          <h2 class="text-xl font-bold border-b pb-3 mb-4 text-gray-800">🛒 我的购物车</h2>
          <div v-if="cartStore.items.length === 0" class="text-gray-400 text-center py-10">购物车空空如也，快去选购吧！</div>
          <div v-else>
            <div v-for="item in cartStore.items" :key="item.id" class="flex justify-between items-center mb-4 bg-white p-3 rounded shadow-sm">
              <div>
                <div class="font-bold text-gray-700 text-sm mb-1">{{ item.name }}</div>
                <div class="text-red-500 font-medium text-xs">¥{{ item.price }} <span class="text-gray-400 ml-1">x {{ item.quantity }}</span></div>
              </div>
              <button @click="cartStore.removeFromCart(item.id)" class="text-red-400 hover:text-red-600 text-sm ml-2">移除</button>
            </div>
            <div class="mt-6 pt-4 border-t-2 border-dashed border-gray-200">
              <div class="flex justify-between items-center font-bold text-lg mb-4">
                <span class="text-gray-700">总计金额：</span><span class="text-red-600 text-2xl">¥{{ cartStore.totalPrice }}</span>
              </div>
              <button @click="checkout" class="w-full bg-red-500 hover:bg-red-600 text-white font-bold py-3 rounded shadow-md transition transform hover:scale-105">立即结算付款</button>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-gray-100 p-6 rounded-lg border">
        <h2 class="text-xl font-bold border-b-2 border-gray-300 pb-3 mb-4 text-gray-800">
          🧾 {{ userStore.userInfo?.role === 'admin' ? '全站订单监控 (数据库直连)' : '我的历史订单' }}
        </h2>
        <table class="w-full text-left bg-white rounded shadow-sm">
          <thead>
            <tr class="bg-gray-200 text-gray-700">
              <th class="p-3 border-b">订单号</th>
              <th class="p-3 border-b">购买用户</th>
              <th class="p-3 border-b">购买明细</th>
              <th class="p-3 border-b">支付总额</th>
              <th class="p-3 border-b">交易时间</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="order in orders" :key="order.id" class="hover:bg-gray-50 border-b">
              <td class="p-3 text-gray-500">#{{ order.id }}</td>
              <td class="p-3 font-bold text-blue-600">{{ order.username }}</td>
              <td class="p-3 text-sm text-gray-600">{{ order.items_detail }}</td>
              <td class="p-3 font-bold text-red-500">¥{{ order.total_price }}</td>
              <td class="p-3 text-xs text-gray-400">{{ order.created_at }}</td>
            </tr>
            <tr v-if="orders.length === 0">
              <td colspan="5" class="p-8 text-center text-gray-400">目前还没有任何订单数据哦~</td>
            </tr>
          </tbody>
        </table>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { useCartStore } from '@/store/cart'
import ProductList from '@/components/ProductList.vue'
import axios from 'axios'

const userStore = useUserStore()
const cartStore = useCartStore() 
const router = useRouter()

const products = ref([])
const orders = ref([]) // 新增：存放订单数据的数组
const searchKey = ref('')
const newItemName = ref('')
const newItemPrice = ref('')

const fetchProducts = async () => {
  try {
    const res = await axios.get('http://localhost:3000/api/products')
    if (res.data.code === 200) { products.value = res.data.data }
  } catch (error) { console.error('获取商品失败', error) }
}

// 新增：向后端拉取订单数据
const fetchOrders = async () => {
  try {
    const res = await axios.get('http://localhost:3000/api/orders', { headers: { Authorization: userStore.token } })
    if (res.data.code === 200) { orders.value = res.data.data }
  } catch (error) { console.error('获取订单失败', error) }
}

onMounted(() => { 
  fetchProducts()
  fetchOrders() // 页面加载时顺便拉取订单
})

const filteredProducts = computed(() => {
  return products.value.filter(product => product.name.toLowerCase().includes(searchKey.value.toLowerCase()))
})

const addProduct = async () => {
  if (!newItemName.value || !newItemPrice.value) return alert('请填写完整信息')
  try {
    await axios.post('http://localhost:3000/api/products', { name: newItemName.value, price: Number(newItemPrice.value) }, { headers: { Authorization: userStore.token } })
    fetchProducts(); newItemName.value = ''; newItemPrice.value = '';
  } catch (error) { alert('上架失败，可能权限不足') }
}

const deleteProduct = async (id) => {
  try {
    await axios.delete(`http://localhost:3000/api/products/${id}`, { headers: { Authorization: userStore.token } })
    fetchProducts()
  } catch (error) { alert('下架失败') }
}

// 核心修改：真实的结算付款，写入数据库
const checkout = async () => {
  if (cartStore.items.length === 0) return alert('购物车是空的！')
  
  // 把购物车里的东西拼接成一个描述字符串，比如 "latiao x1, Vicious x2"
  const details = cartStore.items.map(item => `${item.name} x${item.quantity}`).join(' | ')

  try {
    const res = await axios.post('http://localhost:3000/api/orders', {
      total_price: cartStore.totalPrice,
      items_detail: details
    }, { headers: { Authorization: userStore.token } })

    if (res.data.code === 200) {
      alert(res.data.message)
      cartStore.clearCart()
      fetchOrders() // 支付成功后，立即刷新底部的订单列表！
    }
  } catch (error) {
    alert('支付失败，请检查网络！')
  }
}

const handleLogout = () => {
  userStore.logout()
  cartStore.clearCart() 
  router.push('/login')
}
</script>