<script setup>
// ========== 1. 接收父组件传来的 props ==========
const props = defineProps({
    title: {
        type: String,           // 指定类型为字符串
        default: '默认标题'      // 如果父组件没传，使用默认值
    }
})

// ========== 2. 声明要向父组件触发的事件（子传父的关键） ==========
// defineEmits 返回一个 emit 函数，用于触发自定义事件
// 参数是一个数组，包含所有要触发的事件名
const emit = defineEmits(['sendTitleToParent'])

// ========== 3. 定义触发事件的方法 ==========
const sendTitleToParent = () => {
    // emit(事件名, 要传递的数据)
    // 第一个参数：事件名（必须和 defineEmits 中声明的一致）
    // 第二个参数：要传给父组件的数据（可以是任意类型）
    emit('sendTitleToParent', props.title + '（已被子组件修改）')
}
</script>

<template>
    <div class="SonFooter">
        <h3>{{ props.title }}</h3>
        <Button />
        <button @click="sendTitleToParent">子传父</button>
    </div>
</template>

<style scoped>
.SonFooter {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    height: 100px;
    line-height: 100px;
    text-align: center;
    font-size: 30px;
    margin-bottom: 20px;
    background-color: #e9a7e0;
}
</style>