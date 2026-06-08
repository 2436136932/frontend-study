<script setup>
// 在 Vue3 CompositionAPI 中
// 1. 获取路由对象 router  useRouter
//    const router = useRouter()
// 2. 获取路由参数 route  useRoute
//    const route = useRoute()

import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from './stores/modules/user'
const userStore = useUserStore()  
const router = useRouter()
const route = useRoute()

const golist = () => {
  console.log(router, route)
  router.push('/list')
}
</script>

<template>
  <div>
    <h1>Hello Vue 3!</h1>
    <el-button @click="router.push('/home')">首页</el-button>
    <el-button @click="golist">列表页</el-button>
    <p>当前token: {{ userStore.token }}</p>
    <el-button @click="userStore.setToken('Bearer 1sfrg2ftb3grgrsd4rry5cbe6')">设置token</el-button>
    <el-button @click="userStore.removeToken">清除token</el-button> 
  </div>
</template>

<style scoped></style>
