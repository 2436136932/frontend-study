<script setup>
// 1. 定义 modelValue prop，接收父组件通过 v-model 传来的值
defineProps({
    modelValue: {
        type: String,
        default: ''
    }
})

// 2. 定义 emit 事件，用于向父组件发送更新
const emit = defineEmits(['update:modelValue'])

// 3. 处理 select 变化事件，发送新值给父组件
const handleChange = (event) => {
    emit('update:modelValue', event.target.value)
}
</script>


<template>
    <div>
        <!-- 4. 绑定 modelValue 作为 select 的值 -->
        <!-- 5. 监听 change 事件，触发 handleChange 更新父组件 -->
        <select :value="modelValue" @change="handleChange">
            <option value="1">北京</option>
            <option value="2">合肥</option>
            <option value="3">广州</option>
            <option value="4">深圳</option>
            <option value="5">上海</option>
        </select>
    </div>
</template>

<style scoped>
    select {
        width: 100px;
    }
</style>
