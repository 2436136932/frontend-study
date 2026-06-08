<script setup>
// ====== 子组件：用 defineModel 接收父组件的 v-model ======

// defineModel() 是 Vue 3.4+ 的语法糖，等价于以下两行：
//   const props = defineProps(['modelValue'])
//   const emit = defineEmits(['update:modelValue'])
//
// 它返回一个 ref，读取 = 取父组件的值，写入 = 触发事件通知父组件更新
const modelValue = defineModel()

// 扩展理解：如果不用 defineModel，手动写法如下：
// const props = defineProps(['modelValue'])
// const emit = defineEmits(['update:modelValue'])
//
// 模板中就需要写成：
//   :value="props.modelValue"
//   @input="emit('update:modelValue', $event.target.value)"
</script>

<template>
    <div>
        <!--
      1. :value="modelValue"        → 将父组件的值显示在 input 中（绑定展示）
      2. @input="modelValue = ..."   → 用户输入时，修改 modelValue
           修改 modelValue 底层会触发 emit('update:modelValue', 新值)
           父组件收到后更新 inputValue，形成闭环
    -->
        <input type="text" :value="modelValue" @input="modelValue = $event.target.value" />
    </div>
</template>

<style scoped></style>