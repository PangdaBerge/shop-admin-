<template>
  <div class="space-y-6">
    <!-- ===== 顶部操作栏 ===== -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-4 md:p-6 transition-colors">
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
        <div>
          <h1 class="text-xl md:text-2xl font-bold text-gray-800 dark:text-white">📋 任务看板</h1>
          <p class="text-xs md:text-sm text-gray-400 dark:text-gray-500 mt-1">
            <template v-if="viewMode === 'all'">📊 团队视图 — 所有人的任务</template>
            <template v-else-if="viewMode === 'user'">👤 {{ filterUsername }} 的任务</template>
            <template v-else>📌 我的任务</template>
          </p>
        </div>

        <div class="flex items-center gap-3">
          <!-- 管理员视图切换 -->
          <div v-if="userStore.userInfo?.role === 'admin'" class="flex items-center gap-2">
            <label class="text-xs text-gray-500 dark:text-gray-400 whitespace-nowrap">视图:</label>
            <select
              v-model="viewMode"
              class="text-sm px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"
              @change="onViewChange"
            >
              <option value="mine">📌 我的任务</option>
              <option value="all">📊 团队全部</option>
              <option v-for="u in userList" :key="u" :value="'user:' + u">👤 {{ u }}</option>
            </select>
          </div>

          <button @click="showAddModal = true" class="bg-blue-500 hover:bg-blue-600 text-white font-bold px-4 py-2 rounded-lg transition duration-200 text-sm whitespace-nowrap">
            + 新建任务
          </button>
        </div>
      </div>
    </div>

    <!-- ===== 三列看板 ===== -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-6">
      <!-- 待处理 -->
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-4 transition-colors">
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-bold text-gray-700 dark:text-gray-200">
            <span class="inline-block w-3 h-3 rounded-full bg-yellow-400 mr-2"></span>
            待处理
          </h3>
          <span class="text-xs bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400 px-2 py-0.5 rounded-full">{{ todoTasks.length }}</span>
        </div>
        <div class="space-y-3 min-h-[200px]">
          <div
            v-for="task in todoTasks"
            :key="task.id"
            class="group bg-gray-50 dark:bg-gray-700/50 border border-gray-100 dark:border-gray-600 rounded-lg p-3 hover:shadow-md transition-all cursor-pointer"
            @click="editTask(task)"
          >
            <div class="flex items-start justify-between gap-2">
              <h4 class="font-medium text-gray-800 dark:text-gray-200 text-sm">{{ task.title }}</h4>
              <span :class="priorityBadge(task.priority)" class="text-xs px-1.5 py-0.5 rounded font-medium shrink-0">{{ priorityLabel(task.priority) }}</span>
            </div>
            <p v-if="task.description" class="text-xs text-gray-400 dark:text-gray-500 mt-2 line-clamp-2">{{ task.description }}</p>
            <div class="flex items-center justify-between mt-3 pt-2 border-t border-gray-100 dark:border-gray-600">
              <span class="text-xs text-gray-400">
                <span class="text-gray-500 dark:text-gray-400">👤 {{ task.username }}</span>
                <span v-if="task.assignee && task.assignee !== task.username" class="ml-2 text-gray-400">→ {{ task.assignee }}</span>
              </span>
              <div class="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                <button @click.stop="moveTask(task, 'in_progress')" class="text-xs bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 px-2 py-1 rounded hover:bg-blue-200 dark:hover:bg-blue-900/50 transition-colors">开始</button>
              </div>
            </div>
          </div>
          <div v-if="todoTasks.length === 0" class="text-center text-gray-400 dark:text-gray-500 text-sm py-8">暂无待处理任务</div>
        </div>
      </div>

      <!-- 进行中 -->
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-4 transition-colors">
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-bold text-gray-700 dark:text-gray-200">
            <span class="inline-block w-3 h-3 rounded-full bg-blue-400 mr-2"></span>
            进行中
          </h3>
          <span class="text-xs bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400 px-2 py-0.5 rounded-full">{{ inProgressTasks.length }}</span>
        </div>
        <div class="space-y-3 min-h-[200px]">
          <div
            v-for="task in inProgressTasks"
            :key="task.id"
            class="group bg-gray-50 dark:bg-gray-700/50 border border-gray-100 dark:border-gray-600 rounded-lg p-3 hover:shadow-md transition-all cursor-pointer"
            @click="editTask(task)"
          >
            <div class="flex items-start justify-between gap-2">
              <h4 class="font-medium text-gray-800 dark:text-gray-200 text-sm">{{ task.title }}</h4>
              <span :class="priorityBadge(task.priority)" class="text-xs px-1.5 py-0.5 rounded font-medium shrink-0">{{ priorityLabel(task.priority) }}</span>
            </div>
            <p v-if="task.description" class="text-xs text-gray-400 dark:text-gray-500 mt-2 line-clamp-2">{{ task.description }}</p>
            <div class="flex items-center justify-between mt-3 pt-2 border-t border-gray-100 dark:border-gray-600">
              <span class="text-xs text-gray-400">{{ task.assignee || '未分配' }}</span>
              <div class="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                <button @click.stop="moveTask(task, 'todo')" class="text-xs bg-gray-200 dark:bg-gray-600 text-gray-600 dark:text-gray-300 px-2 py-1 rounded hover:bg-gray-300 dark:hover:bg-gray-500 transition-colors">退回</button>
                <button @click.stop="moveTask(task, 'done')" class="text-xs bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400 px-2 py-1 rounded hover:bg-green-200 dark:hover:bg-green-900/50 transition-colors">完成</button>
              </div>
            </div>
          </div>
          <div v-if="inProgressTasks.length === 0" class="text-center text-gray-400 dark:text-gray-500 text-sm py-8">暂无进行中任务</div>
        </div>
      </div>

      <!-- 已完成 -->
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-4 transition-colors">
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-bold text-gray-700 dark:text-gray-200">
            <span class="inline-block w-3 h-3 rounded-full bg-green-400 mr-2"></span>
            已完成
          </h3>
          <span class="text-xs bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 px-2 py-0.5 rounded-full">{{ doneTasks.length }}</span>
        </div>
        <div class="space-y-3 min-h-[200px]">
          <div
            v-for="task in doneTasks"
            :key="task.id"
            class="group bg-gray-50 dark:bg-gray-700/50 border border-gray-100 dark:border-gray-600 rounded-lg p-3 hover:shadow-md transition-all cursor-pointer"
            @click="editTask(task)"
          >
            <div class="flex items-start justify-between gap-2">
              <h4 class="font-medium text-gray-400 dark:text-gray-500 line-through text-sm">{{ task.title }}</h4>
              <span :class="priorityBadge(task.priority)" class="text-xs px-1.5 py-0.5 rounded font-medium shrink-0 opacity-50">{{ priorityLabel(task.priority) }}</span>
            </div>
            <p v-if="task.description" class="text-xs text-gray-400 dark:text-gray-500 mt-2 line-clamp-2 line-through">{{ task.description }}</p>
            <div class="flex items-center justify-between mt-3 pt-2 border-t border-gray-100 dark:border-gray-600">
              <span class="text-xs text-gray-400">{{ task.assignee || '未分配' }}</span>
              <div class="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                <button @click.stop="moveTask(task, 'in_progress')" class="text-xs bg-gray-200 dark:bg-gray-600 text-gray-600 dark:text-gray-300 px-2 py-1 rounded hover:bg-gray-300 dark:hover:bg-gray-500 transition-colors">重开</button>
                <button @click.stop="deleteTask(task.id)" class="text-xs bg-red-100 dark:bg-red-900/30 text-red-500 dark:text-red-400 px-2 py-1 rounded hover:bg-red-200 dark:hover:bg-red-900/50 transition-colors">删除</button>
              </div>
            </div>
          </div>
          <div v-if="doneTasks.length === 0" class="text-center text-gray-400 dark:text-gray-500 text-sm py-8">暂无已完成任务</div>
        </div>
      </div>
    </div>

    <!-- ===== 新建/编辑任务弹窗 ===== -->
    <div v-if="showAddModal || editingTask" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4" @click.self="closeModal">
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-2xl w-full max-w-md p-6 transition-colors">
        <h2 class="text-lg font-bold text-gray-800 dark:text-white mb-4">
          {{ editingTask ? '编辑任务' : '新建任务' }}
        </h2>
        <form @submit.prevent="saveTask" class="space-y-4">
          <div>
            <label class="block text-xs font-semibold text-gray-500 dark:text-gray-400 mb-1">任务标题 *</label>
            <input v-model="form.title" type="text" required class="w-full px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm transition-colors" placeholder="输入任务标题...">
          </div>
          <div>
            <label class="block text-xs font-semibold text-gray-500 dark:text-gray-400 mb-1">描述</label>
            <textarea v-model="form.description" rows="2" class="w-full px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm transition-colors resize-none" placeholder="任务描述 (可选)"></textarea>
          </div>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-xs font-semibold text-gray-500 dark:text-gray-400 mb-1">优先级</label>
              <select v-model="form.priority" class="w-full px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm transition-colors">
                <option value="low">低</option>
                <option value="medium">中</option>
                <option value="high">高</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-semibold text-gray-500 dark:text-gray-400 mb-1">负责人</label>
              <input v-model="form.assignee" type="text" class="w-full px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm transition-colors" placeholder="负责人名称">
            </div>
          </div>
          <div>
            <label class="block text-xs font-semibold text-gray-500 dark:text-gray-400 mb-1">状态</label>
            <select v-model="form.status" class="w-full px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm transition-colors">
              <option value="todo">待处理</option>
              <option value="in_progress">进行中</option>
              <option value="done">已完成</option>
            </select>
          </div>
          <div class="flex gap-3 pt-2">
            <button type="submit" class="flex-1 bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 rounded-lg transition duration-200 text-sm">
              {{ editingTask ? '保存修改' : '创建任务' }}
            </button>
            <button type="button" @click="closeModal" class="flex-1 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 font-bold py-2 rounded-lg transition duration-200 text-sm">
              取消
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/store/user'
import axios from 'axios'

const userStore = useUserStore()
const API = 'http://localhost:3000/api'

const tasks = ref([])
const userList = ref([])
const viewMode = ref('mine')
const filterUsername = ref('')
const showAddModal = ref(false)
const editingTask = ref(null)

const form = ref({
  title: '',
  description: '',
  status: 'todo',
  priority: 'medium',
  assignee: ''
})

const todoTasks = computed(() => tasks.value.filter(t => t.status === 'todo'))
const inProgressTasks = computed(() => tasks.value.filter(t => t.status === 'in_progress'))
const doneTasks = computed(() => tasks.value.filter(t => t.status === 'done'))

// 获取用户列表 (仅 admin)
const fetchUsers = async () => {
  if (userStore.userInfo?.role !== 'admin') return
  try {
    const res = await axios.get(`${API}/users`, {
      headers: { Authorization: userStore.token }
    })
    if (res.data.code === 200) userList.value = res.data.data
  } catch (e) { console.error('获取用户列表失败', e) }
}

const fetchTasks = async () => {
  try {
    const params = {}
    if (viewMode.value === 'all') {
      params.view = 'all'
    } else if (viewMode.value === 'user') {
      params.view = 'user'
      params.username_filter = filterUsername.value
    }
    // viewMode === 'mine' 时不传参数，后端默认返回当前用户自己的任务

    const res = await axios.get(`${API}/tasks`, {
      params,
      headers: { Authorization: userStore.token }
    })
    if (res.data.code === 200) tasks.value = res.data.data
  } catch (e) { console.error('获取任务失败', e) }
}

const onViewChange = () => {
  if (viewMode.value.startsWith('user:')) {
    filterUsername.value = viewMode.value.split(':')[1]
    viewMode.value = 'user'
  }
  fetchTasks()
}

onMounted(() => {
  fetchUsers()
  fetchTasks()
})

const priorityBadge = (p) => ({
  high: 'bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400',
  medium: 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-600 dark:text-yellow-400',
  low: 'bg-gray-100 dark:bg-gray-600 text-gray-500 dark:text-gray-400'
}[p] || '')

const priorityLabel = (p) => ({ high: '高', medium: '中', low: '低' }[p] || '')

const moveTask = async (task, newStatus) => {
  try {
    await axios.put(`${API}/tasks/${task.id}`, { status: newStatus }, { headers: { Authorization: userStore.token } })
    fetchTasks()
  } catch (e) { alert('移动失败') }
}

const deleteTask = async (id) => {
  if (!confirm('确定删除该任务吗？')) return
  try {
    await axios.delete(`${API}/tasks/${id}`, { headers: { Authorization: userStore.token } })
    fetchTasks()
  } catch (e) { alert('删除失败') }
}

const editTask = (task) => {
  editingTask.value = task
  form.value = {
    title: task.title,
    description: task.description || '',
    status: task.status,
    priority: task.priority,
    assignee: task.assignee || ''
  }
}

const saveTask = async () => {
  try {
    if (editingTask.value) {
      await axios.put(`${API}/tasks/${editingTask.value.id}`, form.value, { headers: { Authorization: userStore.token } })
    } else {
      await axios.post(`${API}/tasks`, form.value, { headers: { Authorization: userStore.token } })
    }
    closeModal()
    fetchTasks()
  } catch (e) { alert('保存失败') }
}

const closeModal = () => {
  showAddModal.value = false
  editingTask.value = null
  form.value = { title: '', description: '', status: 'todo', priority: 'medium', assignee: '' }
}
</script>
