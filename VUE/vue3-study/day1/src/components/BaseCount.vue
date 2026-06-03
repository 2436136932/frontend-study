<script setup>
import { ref } from 'vue'

const count = ref(0)
</script>

<template>
    <div class="BaseCount">
        <button @click="count++">增加</button>
        <p>当前计数: {{ count }}</p>
        <button @click="count--">减少</button>
    </div>
</template>

<style scoped>
.BaseCount {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    height: 60px;
    line-height: 60px;
    text-align: center;
    font-size: 30px;
    margin-bottom: 20px;
    background-color: #e9a7e0;
}
</style>