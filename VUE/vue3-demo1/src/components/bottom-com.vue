<script setup>
import { inject } from 'vue'

// ====== inject：接收顶层（App）提供的数据 ======
//  inject('key', defaultValue?) — 第二个参数可设默认值（没有 provide 时使用）

// 1. 接收普通字符串 "pink"
const color = inject('color')

// 2. 接收响应式数据 count（顶层每秒自动减 1）
const count = inject('count')

// 3. 接收函数（点击按钮时调用，修改顶层的 count）
const addCount = inject('addCount')
</script>

<template>
    <div class="bottom">
        <h3>我是底层组件，颜色是{{ color }}，计数是{{ count }}</h3>
        <!-- 调用顶层传递过来的函数，修改顶层的数据 -->
        <button @click="addCount(100)">增加</button>
    </div>
</template>

<style scoped>
.bottom {
    height: 100px;
    width: 100%;
    background-color: aquamarine;
    margin: 0px auto;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
}
</style>
