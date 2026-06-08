/**
 * user.js —— 用户信息 Store（组合式 Setup Store）
 * ------------------------------------------------------------
 * 本文件演示 Pinia 组合式写法中更复杂的场景：
 *   1. 多个 ref 状态管理
 *   2. 多个 computed 派生数据
 *   3. 带参数的方法
 *   4. 异步请求（async/await）
 *   5. loading 和 error 状态管理
 *
 * 学习目标：
 *   - 掌握多个状态的组织方式
 *   - 掌握异步请求在 Store 中的标准写法
 *   - 理解 try/catch/finally 在异步请求中的作用
 */

// ======================================================================
// 1. 导入依赖
// ======================================================================
// axios：用于发送 HTTP 请求
import axios from 'axios'

// ref：创建响应式数据
// computed：创建计算属性
import { computed, ref } from 'vue'

// defineStore：Pinia 核心 API
import { defineStore } from 'pinia'

// ======================================================================
// 2. 定义 Store
// ======================================================================
// 组件中使用方式：
//   import { useUserStore } from './stores/user'
//   const userStore = useUserStore()
//   userStore.name              // 读取姓名
//   userStore.fetchChannels()   // 调用异步方法
export const useUserStore = defineStore('user', () => {
  // ==================================================================
  // 3. 定义响应式状态（多个 ref）
  // ==================================================================

  // 用户名，初始值为 '默认用户'
  const name = ref('默认用户')

  // 年龄，初始值为 18
  const age = ref(18)

  // 频道列表，初始值为空数组
  // 这个数据会通过接口请求获取
  const channelList = ref([])

  // 加载状态，初始值为 false
  // 用于告诉页面当前是否正在请求数据
  const loading = ref(false)

  // 错误信息，初始值为空字符串
  // 用于存储请求失败时的错误提示
  const error = ref('')

  // ==================================================================
  // 4. 定义计算属性（多个 computed）
  // ==================================================================

  // 用户描述：把姓名和年龄拼成一句话
  // 例如：'张三，25 岁'
  const description = computed(() => `${name.value}，${age.value} 岁`)

  // 频道数量：统计频道列表的长度
  // 例如：channelList 有 10 个元素，channelCount 就是 10
  const channelCount = computed(() => channelList.value.length)

  // ==================================================================
  // 5. 定义普通方法（同步）
  // ==================================================================

  // 更新用户名
  // @param {string} newName - 新的用户名
  const updateName = (newName) => {
    name.value = newName
  }

  // 年龄加 1
  const growUp = () => {
    age.value++
  }

  // ==================================================================
  // 6. 定义异步方法（async/await）
  // ==================================================================
  // 获取频道列表
  // 这是一个异步方法，会发送 HTTP 请求获取数据
  //
  // 标准流程：
  //   1. 开启 loading
  //   2. 清空旧错误
  //   3. 发送请求
  //   4. 成功时更新数据
  //   5. 失败时记录错误
  //   6. 最后关闭 loading
  const fetchChannels = async () => {
    // 第一步：开启加载状态，清空旧错误
    loading.value = true
    error.value = ''

    try {
      // 第二步：发送 HTTP 请求
      // 注意：这里请求的是 '/api/v1_0/channels'
      // 实际会被 Vite 代理转发到 'http://geek.itheima.net/v1_0/channels'
      const res = await axios.get('/api/v1_0/channels')

      // 第三步：请求成功，更新频道列表
      // 根据接口返回的数据结构，真正的数据在 res.data.data.channels
      channelList.value = res.data.data.channels
    } catch (err) {
      // 第四步：请求失败，记录错误信息
      // err 是错误对象，这里我们只保存一个友好的错误提示
      error.value = '获取频道列表失败，请检查代理配置或接口状态'
      channelList.value = []
    } finally {
      // 第五步：无论成功失败，都关闭加载状态
      // finally 中的代码一定会执行，适合做收尾工作
      loading.value = false
    }
  }

  // ==================================================================
  // 7. 通过 return 暴露数据和方法
  // ==================================================================
  return {
    // 状态
    name,
    age,
    channelList,
    loading,
    error,

    // 计算属性
    description,
    channelCount,

    // 方法
    updateName,
    fetchChannels,
    growUp,
  }
})
