<script setup>
import { ref, watch } from 'vue'

const count = ref(0)
const nickName = ref('张三')
// 1. 监视单个数据的变化
// watch(ref对象, (newValue, oldValue) => { ... })

// watch(count, (newValue, oldValue) => {
//   console.log(newValue, oldValue)
// })
// watch(nickName, (newValue, oldValue) => {
//   console.log(newValue, oldValue)
// })

// 2. 监视多个数据的变化
// watch([ref对象1, ref对象2], (newArr, oldArr) => { ... })
// watch([count, nickName], (newArr, oldArr) => {
//   console.log(newArr, oldArr)
// }, {
//   immediate: true
// }
// )

// 3.immediate: true 选项
// 监视数据变化时，会立即执行一次回调函数，
// 用于初始化数据
// watch(count, (newValue, oldValue) => {
//   console.log(newValue, oldValue)
// }, {
//   immediate: true
// }
// )

// 4.deep: true 选项
// 监视对象数据的变化时，会递归监视对象的所有属性，
const info = ref({
  count: 0,
  nickName: '张三'
})

const setInfo = () => {
  info.value.count++  // ✅ 在函数里修改
}
watch(info, (newObj, oldObj) => {
  console.log(newObj, oldObj)
}, {
  deep: true
})

// 5. 监视数组数据的变化
const user = ref({
  name: '张三',
  age: 18
})
const setUser = () => {
  user.value.age++  // ✅ 在函数里修改
}
watch(() => user.value.age, (newValue, oldValue) => {
  console.log(newValue, oldValue)
})

</script>

<template>
  <div>
    <h1>count: {{ count }}</h1>
    <h1>nickName: {{ nickName }}</h1>
    <button @click="count++">点击我</button>
    <button @click="nickName = '李四'">点击我2</button>
    <hr>
    <h1>{{ info }}</h1>
    <button @click="setInfo">点击我3</button>
    <button @click="info.nickName = '王五'">点击我4</button>
    <hr>
    <h1>{{ user }}</h1>
    <button @click="setUser">点击我5</button>
  </div>
</template>

<style scoped></style>