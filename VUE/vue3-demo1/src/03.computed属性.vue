<script setup>
import { ref, computed } from 'vue'
//数据
const count = ref([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
//标志位
const flag = ref(false)
//计算属性
const doubleCount = computed(() => {
    return count.value.filter(item => item % 2 === 0)
})
//函数
const logMessage = () => {
    flag.value = !flag.value
    if(flag.value) {
        console.log(doubleCount.value)
    }
}
//模板中使用计算属性
//模板中使用函数
//模板中使用数据
</script>

<template>
    <div>
        <h1>{{ count }}</h1>
        <h1 v-if="flag">{{ doubleCount }}</h1>
        <button @click="logMessage">点击计算</button>
    </div>
</template>

<style scoped></style>



<!-- 不常用 -->
<!-- <script setup>
import { ref, computed } from 'vue'

const count = ref(1)

// computed 的 get/set 写法：传入一个包含 get 和 set 的对象
const plus = computed({
  // getter：读取时触发，返回计算后的值
  get() {
    return count.value + 1
  },
  // setter：赋值时触发，newVal 是赋的值
  set(newVal) {
    count.value = newVal - 1
  }
})
</script>

<template>
  <div>
    <h1>count: {{ count }}</h1>
    <h1>plus: {{ plus }}</h1>
    <button @click="plus = 100">点击我</button>
  </div>
</template>

<style scoped>

</style> -->