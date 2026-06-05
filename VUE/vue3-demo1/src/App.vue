<script setup>
import TestCom from './components/test-com.vue'
import { ref } from 'vue'

// ====== 1. 模板引用 — 操作 DOM 元素 ======

// 创建 ref 变量，变量名和模板中 ref="inputRef" 一致
const inputRef = ref(null)
const fn = () => {
    // inputRef.value 就是真实的 DOM 元素
    inputRef.value.focus()
}

// ====== 2. 模板引用 — 获取子组件实例 ======

const testComRef = ref(null)
const getCom = () => {
    // testComRef.value 就是子组件实例
    console.log(testComRef.value)           // proxy 对象
    console.log(testComRef.value.count)     // 访问子组件暴露的 count
    testComRef.value.sayHi()                // 调用子组件暴露的方法
}
</script>

<template>
  <div>
    <!-- ref="inputRef" → 把 input 元素绑定到 inputRef 变量 -->
    <input ref="inputRef" type="text">
    <button @click="fn">点击聚焦</button>
  </div>
  <!-- ref="testComRef" → 把子组件实例绑定到 testComRef 变量 -->
  <TestCom ref="testComRef" />
  <button @click="getCom">获取子组件</button>
</template>

<style scoped>

</style>