<script setup>
// 1. 导入子组件
import BaseSelect from './components/BaseSelect.vue'

// 2. 导入 Vue 的响应式 API
import { ref } from 'vue'

// 3. 创建响应式数据，初始值为 '2'
const selected = ref('2')
</script>

<template>
  <div class="App">
    <!-- 4. 使用 v-model 双向绑定，将 selected 传给子组件 -->
    <BaseSelect v-model="selected" />

    <!-- 5. 显示当前选中的值，实时更新 -->
    <p>当前选中的值: {{ selected }}</p>
  </div>

</template>

<style scoped></style>
<!--
========== 双向绑定的完整流程 ==========

步骤1: 父组件创建响应式数据
  - selected = ref('2') 创建了一个响应式变量
  - 初始值为 '2'，对应下拉框的"选项2"

步骤2: 父组件通过 v-model 传给子组件
  - <BaseSelect v-model="selected" />
  - v-model 是语法糖，等价于:
    :modelValue="selected" @update:modelValue="selected = $event"

步骤3: 子组件接收 modelValue prop
  - defineProps({ modelValue: { type: String, default: '' } })
  - 子组件通过 prop 接收父组件的值

步骤4: 子组件的 select 显示当前值
  - <select :value="modelValue" @change="handleChange">
  - :value 绑定 prop 值，使下拉框显示当前选中项

步骤5: 用户改变选项时触发 change 事件
  - 用户在下拉框中选择不同的选项
  - @change="handleChange" 监听这个事件

步骤6: 子组件发送 emit 事件给父组件
  - emit('update:modelValue', event.target.value)
  - 将新选中的值发送回父组件

步骤7: 父组件的 selected 更新
  - v-model 自动接收 update:modelValue 事件
  - selected 的值被更新为新选中的值
  - 页面重新渲染，显示新的值

步骤8: 循环回到步骤4
  - 子组件的 :value="modelValue" 会显示新的值
  - 下拉框的显示会同步更新

========== 总结 ==========
这就是 Vue 3 中 v-model 双向绑定的完整机制：
父组件数据 ↔ v-model ↔ 子组件 prop ↔ emit 事件 ↔ 父组件数据
-->