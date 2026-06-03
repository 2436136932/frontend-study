<!-- 加上setup属性，允许在setup里面直接编写组合式API -->
<script setup>
import { ref } from 'vue'  // 导入 ref，用于创建响应式数据
import Header from './components/Header.vue'
import Main from './components/Main.vue'
import SonFooter from './components/SonFooter.vue'
import BaseCount from './components/BaseCount.vue'

// ========== 一、创建响应式数据（父传子的数据源） ==========
// 用 ref 包裹，这样数据变化时视图会自动更新
const title = ref('父组件传子组件标题')

// ========== 二、定义处理子组件传来数据的方法（子传父的接收端） ==========
// 参数 newTitle 就是子组件通过 emit 传递过来的数据
const handleTitleFromChild = (newTitle) => {
    console.log('子组件传来的数据:', newTitle)
    // 修改响应式数据时，需要通过 .value 访问
    title.value = newTitle
}
</script>

<template>
  <div class="App">
    <!-- 头部组件 -->
    <Header />
    <!-- 主体组件 -->
    <Main />
    <!--
      底部组件（演示父子组件通信）
      【父传子】通过 :title 将数据传给子组件（props）
      【子传父】通过 @sendTitleToParent 监听子组件触发的事件
         - @事件名="处理函数" 是 v-on:事件名="处理函数" 的简写
         - 当子组件调用 emit('sendTitleToParent', 数据) 时
         - 父组件的 handleTitleFromChild 函数会被调用，并接收到数据
    -->
    <SonFooter :title="title" @sendTitleToParent="handleTitleFromChild" />
    <!-- 基础计数组件 -->
    <BaseCount />
    <BaseCount />
  </div>
</template>

<style scoped>
.App {
  width: 600px;
  height: 700px;
  background-color: skyblue;
  margin: 0 auto;
  padding: 20px;
}
</style>
