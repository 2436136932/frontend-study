<script setup>
import { onMounted } from 'vue'

// beforeCreate 和 created 的相关代码
// 一律放在 setup 中执行

const getList = () => {
  setTimeout(() => {
    console.log('模拟发送请求，获取数据')
  }, 2000)
}
// 一进入页面的请求
getList()

// 如果有些代码需要在 mounted 生命周期中执行
onMounted(() => {
  console.log('mounted 生命周期函数 - 逻辑 1')
})

// 写成函数的调用方式，可以调用多次，并不会冲突，而是按照顺序
onMounted(() => {
  console.log('mounted 生命周期函数 - 逻辑 2')
})

// ==========  Vue3 全部生命周期钩子（组合式 API ） ==========

// ★ setup  — 相当于 Vue 2 的 beforeCreate + created
//    所有写在 <script setup> 顶层（不是钩子里的）代码都在这个阶段执行

// 1. onBeforeMount  — DOM 挂载之前
//    onBeforeMount(() => { console.log('DOM 还没挂载') })

// 2. onMounted      — DOM 挂载完成（已用在上方）
//    onMounted(() => { console.log('DOM 已挂载') })

// 3. onBeforeUpdate — 数据变化，DOM 更新之前
//    onBeforeUpdate(() => { console.log('数据变了，DOM 还没更新') })

// 4. onUpdated      — DOM 更新完成
//    onUpdated(() => { console.log('DOM 已更新') })

// 5. onBeforeUnmount — 组件卸载之前（清理定时器、解绑事件等）
//    onBeforeUnmount(() => { console.log('组件即将卸载') })

// 6. onUnmounted    — 组件卸载完成
//    onUnmounted(() => { console.log('组件已卸载') })
</script>

<template>
  <div>
    
  </div>
</template>

<style scoped>

</style>