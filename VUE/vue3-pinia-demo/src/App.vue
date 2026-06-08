<!--
  ====================================================================
  App.vue —— 根组件，演示如何在 Vue 组件中使用 Pinia 组合式 Store
  ====================================================================

  学习目标：
    1. 掌握如何在组件中引入和使用 Store
    2. 掌握 storeToRefs 的作用和用法
    3. 掌握如何在模板中渲染 Store 的数据
    4. 掌握如何通过事件调用 Store 的 actions

  Pinia 在组件中的使用三步曲：
    步骤一：import 引入 useXxxStore 函数
    步骤二：调用 useXxxStore() 获取 Store 实例
    步骤三：通过 Store 实例访问状态、计算属性和方法
-->

<script setup>
// ====================================================================
// 脚本部分（<script setup> 语法）
// ====================================================================
// 这是 Vue3 的组合式 API 写法（Composition API）
// <script setup> 中的代码在组件创建时只执行一次

// ----------------------------------------------------------
// 1. 引入 Store
// ----------------------------------------------------------
// 从对应的文件中导入 useCounterStore 和 useUserStore
// 注意：需要写完整的相对路径（./stores/xxx）
import { useCounterStore } from './stores/counter'
import { useUserStore } from './stores/user'

// ----------------------------------------------------------
// 2. 引入 storeToRefs
// ----------------------------------------------------------
// storeToRefs 是 Pinia 提供的工具函数
// 作用：解构 Store 时保持响应性
//
// 为什么需要它？
//   如果直接解构：const { count } = counterStore
//   这样解构出来的 count 会丢失响应式，页面不会自动更新
//
// 正确做法：
//   const { count } = storeToRefs(counterStore)
//   这样 count 仍然是响应式的
//
// 注意：
//   - state 和 getters 需要用 storeToRefs 解构
//   - actions（方法）可以直接解构，不需要 storeToRefs
import { storeToRefs } from 'pinia'

// ----------------------------------------------------------
// 3. 获取 Store 实例
// ----------------------------------------------------------
// 调用 useCounterStore() 会返回一个 Store 实例
// 每次调用都返回同一个 Store 实例（单例模式）
// 也就是说，所有组件共享同一个 counterStore / userStore
const counterStore = useCounterStore()
const userStore = useUserStore()

// ----------------------------------------------------------
// 4. 使用 storeToRefs 解构（保持响应性）
// ----------------------------------------------------------
// 这里只解构了 count，因为模板中直接使用了 count
// doubleCount 没有解构，所以模板中用 counterStore.doubleCount
const { count } = storeToRefs(counterStore)

// ----------------------------------------------------------
// 补充：actions 可以直接解构
// ----------------------------------------------------------
// 例如：
//   const { increment, decrement, reset } = counterStore
// 这样也是可以的，因为函数本身不需要响应式
</script>

<template>
  <!--
    ================================================================
    模板部分
    ================================================================
    在模板中使用 Store 的属性和方法与使用普通数据一样

    核心用法：
      - {{ count }}                     → 渲染通过 storeToRefs 解构的数据
      - {{ counterStore.doubleCount }} → 渲染 Store 中的计算属性
      - @click="counterStore.increment" → 调用 action
  -->
  <div class="app">
    <h1>Vue3 + Pinia</h1>

    <!-- ========================================================= -->
    <!-- 卡片一：计数器 —— 演示最基本的 ref + computed + actions   -->
    <!-- ========================================================= -->
    <div class="card">
      <h2>计数器</h2>

      <!-- 使用 storeToRefs 解构出来的 count，直接访问即可 -->
      <p class="count">Count: {{ count }}</p>

      <!-- 直接通过 counterStore 访问计算属性 -->
      <!-- 注意：getter 在模板中不加括号，它本身是属性不是方法 -->
      <p class="double">Double: {{ counterStore.doubleCount }}</p>

      <div class="buttons">
        <!-- 点击按钮调用 action 方法，加括号表示执行 -->
        <button @click="counterStore.increment">+1</button>
        <button @click="counterStore.decrement">-1</button>
        <button @click="counterStore.reset">重置</button>
      </div>
    </div>

    <!-- ========================================================= -->
    <!-- 卡片二：用户信息 —— 演示多个状态和带参数的方法           -->
    <!-- ========================================================= -->
    <div class="card">
      <h2>用户信息</h2>

      <!-- 通过 userStore 访问状态和计算属性 -->
      <p>姓名：{{ userStore.name }}</p>
      <p>年龄：{{ userStore.age }}</p>
      <p>描述：{{ userStore.description }}</p>

      <div class="buttons">
        <!-- 调用 action 时传参：userStore.updateName('张三') -->
        <button @click="userStore.updateName('张三')">改名张三</button>
        <button @click="userStore.updateName('李四')">改名李四</button>
        <button @click="userStore.growUp()">+1 岁</button>
      </div>
    </div>

    <!-- ========================================================= -->
    <!-- 卡片三：频道列表 —— 演示异步请求和列表渲染               -->
    <!-- ========================================================= -->
    <div class="card">
      <h2>频道列表接口练习</h2>
      <p>接口地址：http://geek.itheima.net/v1_0/channels</p>
      <p>频道数量：{{ userStore.channelCount }}</p>

      <div class="buttons">
        <!--
          点击按钮调用异步方法
          :disabled="userStore.loading" 表示加载中时禁用按钮
          {{ userStore.loading ? '加载中...' : '获取频道列表' }} 动态显示按钮文字
        -->
        <button @click="userStore.fetchChannels()" :disabled="userStore.loading">
          {{ userStore.loading ? '加载中...' : '获取频道列表' }}
        </button>
      </div>

      <!-- 如果有错误信息，显示错误 -->
      <p v-if="userStore.error" class="error">{{ userStore.error }}</p>

      <!-- 如果有频道数据，渲染列表 -->
      <!-- v-if="userStore.channelList.length" 表示有数据时才显示 -->
      <ul v-if="userStore.channelList.length" class="channel-list">
        <!-- v-for 遍历频道列表，item.id 作为 key -->
        <li v-for="item in userStore.channelList" :key="item.id">
          {{ item.id }} - {{ item.name }}
        </li>
      </ul>
    </div>

    <!-- ========================================================= -->
    <!-- 卡片四：Pinia 特点总结                                     -->
    <!-- ========================================================= -->
    <div class="card">
      <h2>Pinia 特点</h2>
      <ul>
        <li>完整的 TypeScript 支持</li>
        <li>轻量级（~1KB）</li>
        <li>支持 Vue DevTools</li>
        <li>模块化设计，每个 Store 独立</li>
        <li>支持组合式 API 写法</li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
/*
  scoped 样式：样式只对当前组件生效，不会污染全局
  这是 Vue 单文件组件（SFC）的特性
*/
.app {
  max-width: 760px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}
h1 {
  color: #42b883;
  margin-bottom: 2rem;
}
.card {
  background: #f5f5f5;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
.card h2 {
  margin-top: 0;
  color: #333;
}
.count {
  font-size: 2rem;
  font-weight: bold;
  color: #42b883;
}
.double {
  color: #888;
}
.buttons {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
  margin-top: 1rem;
  flex-wrap: wrap;
}
button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  background: #42b883;
  color: white;
  cursor: pointer;
  font-size: 1rem;
  transition: background 0.2s;
}
button:hover {
  background: #38a173;
}
button:disabled {
  background: #9acfb8;
  cursor: not-allowed;
}
ul {
  text-align: left;
  list-style: none;
  padding: 0;
}
ul li {
  padding: 0.3rem 0;
}
.channel-list {
  margin-top: 1rem;
  max-height: 280px;
  overflow: auto;
  border-top: 1px solid #ddd;
  padding-top: 0.8rem;
}
.error {
  color: #e53e3e;
  margin-top: 1rem;
}
</style>
