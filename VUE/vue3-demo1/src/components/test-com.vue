<script setup>
import { ref } from 'vue'

// ====== 子组件内部数据和方法 ======

const count = 999
const sayHi = () => {
    console.log('hi')
}

// ====== defineExpose：暴露数据和方法给父组件 ======
// 父组件通过 ref="testComRef" 获取子组件实例后，
// 只能访问到这里暴露的内容（count / sayHi）
defineExpose({
    count,
    sayHi
})
</script>

<template>
    <div>
        测试子组件-{{ count }}
    </div>
</template>

<style scoped></style>