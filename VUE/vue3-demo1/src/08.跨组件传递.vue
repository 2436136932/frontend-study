<script setup>
import CenterCom from './components/center-com.vue'
import { provide, ref } from 'vue'

// ====== provide / inject 跨层级传递数据 ======
//  顶层（App）用 provide 提供数据
//  底层（BottomCom）用 inject 接收数据
//  中间层（CenterCom）不需要管，自动穿透

// 1. 传递普通数据（非响应式）
provide('color', 'pink')

// 2. 传递响应式数据
const count = ref(5000)
provide('count', count)

// 每秒自动减 1，测试底层能否收到响应式更新
setInterval(() => {
    count.value -= 1
}, 1000)

// 3. 传递函数（底层调用此函数来修改顶层的 count）
const addCount = (num) => {
    count.value += num
}
provide('addCount', addCount)
</script>

<template>
    <div>
        <h1>我是顶层组件</h1>
    </div>
    <!-- 中间层组件内部又引入了 BottomCom，形成：App → CenterCom → BottomCom -->
    <CenterCom />
</template>

<style scoped>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

div {
    height: 100px;
    width: 100%;
    background-color: pink;
    margin: 10px auto;
    margin-bottom: 20px;
    line-height: 100px;
    text-align: center;
}
</style>