<script setup>
// ====== 父组件 ======

// 1. 引入子组件
import Son from './components/06.子组件son.vue/index.js'
import { ref } from 'vue'

// 2. 父组件自己的数据
const count = ref(10000)

// 3. 父组件自己用的方法（增加金额）
const getCount = () => {
    count.value += 1000
    return count.value
}

// 4. 父组件接收子组件触发的事件
//    changeFn 作为回调传给子组件，子组件花钱后通知父组件更新 count
const changeFn = (newCount) => {
    count.value -= newCount
}
</script>

<template>
    <div>
        <h3>父组件
            <button @click="getCount()">增加</button>
        </h3>
        <!-- 
            父传子：car 是静态 prop，count 是动态 prop（响应式）
            子传父：@changeMoney 监听子组件触发的自定义事件
        -->
        <Son @changeMoney="changeFn" car="父传子——奔驰" :count="count" />
    </div>
</template>

<style scoped>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}
</style>