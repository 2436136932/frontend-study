<script setup>
import MyInput from './components/my-input.vue'
import { ref } from 'vue'

// ====== 父组件：使用 v-model 实现双向绑定 ======

// 1. 定义一个响应式数据
const inputValue = ref('123456')

// 2. 用 v-model 绑定到子组件上
//    <MyInput v-model="inputValue" />
//    等价于：
//    <MyInput :modelValue="inputValue" @update:modelValue="inputValue = $event" />
//
//    父传子：:modelValue  →  子组件接收 inputValue 的值
//    子传父：@update:modelValue  →  子组件修改后通知父组件更新
</script>

<template>
    <div>
        <!-- v-model 的本质是 :modelValue + @update:modelValue 的语法糖 -->
        <MyInput v-model="inputValue" />
        <p>{{ inputValue }}</p>
    </div>
</template>

<style scoped></style>