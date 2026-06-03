<script setup>
import { ref, nextTick } from 'vue'

const isShow = ref(false)
const title = ref('头部组件')
const tempTitle = ref('')
const inputRef = ref(null)

const handleEditClick = async () => {
    isShow.value = true
    await nextTick()
    inputRef.value.focus()
}
</script>

<template>
    <div class="Header">
        <div v-if="isShow">
            <input type="text" ref="inputRef" v-model="tempTitle">
        </div>
        <div v-else class="Header-content"> 
            <h1>{{title}}</h1>
            <button @click="handleEditClick" >编辑</button>
        </div>
    </div>
</template>

<style scoped>
.Header {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 60px;
    padding: 0 20px;
    background-color: #8064a2;
    color: #fff;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.Header-content {
    display: flex;
    align-items: center;
    justify-content: center;
}

.Header h1 {
    font-size: 20px;
    font-weight: 600;
    margin: 0 12px 0 0;
}

.Header input {
    height: 36px;
    width: 240px;
    padding: 0 12px;
    border: none;
    border-radius: 6px;
    font-size: 14px;
    outline: none;
}

.Header input:focus {
    box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.5);
}

.Header button {
    height: 36px;
    padding: 0 16px;
    border: 2px solid #fff;
    border-radius: 6px;
    background: transparent;
    color: #fff;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s;
}

.Header button:hover {
    background: #fff;
    color: #8064a2;
}
</style>
