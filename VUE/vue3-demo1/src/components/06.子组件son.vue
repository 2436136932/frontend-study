<script setup>
// ====== 子组件 ======

// 1. defineProps：接收父组件传过来的数据
//    父组件 :car="..." :count="..." → 子组件用 props.car / props.count 接收
const props = defineProps({
    car: String,
    count: Number
})

// 在 JS 中通过 props.xxx 访问父组件传来的值
console.log(props.car)
console.log(props.count)

// 2. defineEmits：定义子组件可以触发的事件
//    父组件 @changeMoney="changeFn" → 子组件用 emit('changeMoney', ...) 触发
const emit = defineEmits(['changeMoney'])

// 3. 子组件自己的方法：花钱 → 通知父组件金额减少
const buy = () => {
    // 触发自定义事件，把 500 传给父组件
    emit('changeMoney', 500)
}
</script>

<template>
    <div>
        <h3>子组件-{{ car }}-{{ count }}
            <button @click="buy">花钱</button>
        </h3>
    </div>
</template>

<style scoped>
h3 {
    border: 1px solid rgb(149, 209, 161);
    color: rgb(244, 172, 172);
}
</style>