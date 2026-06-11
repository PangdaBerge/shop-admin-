import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCartStore = defineStore('cart', () => {
  const items = ref([]) // 存放在购物车里的商品

  // 加入购物车
  const addToCart = (product) => {
    const existItem = items.value.find(item => item.id === product.id)
    if (existItem) {
      existItem.quantity++ // 如果已经有了，数量加1
    } else {
      items.value.push({ ...product, quantity: 1 }) // 如果没有，新增一项
    }
  }

  // 从购物车移除
  const removeFromCart = (productId) => {
    items.value = items.value.filter(item => item.id !== productId)
  }

  // 清空购物车
  const clearCart = () => {
    items.value = []
  }

  // 计算总价
  const totalPrice = computed(() => {
    return items.value.reduce((sum, item) => sum + item.price * item.quantity, 0)
  })

  return { items, addToCart, removeFromCart, clearCart, totalPrice }
})