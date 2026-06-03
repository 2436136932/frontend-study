<script setup>
import { ref } from 'vue'

const msg = ref('Day2 学习开始 🚀')
</script>

<template>
  <div class="app">
    <h1>{{ msg }}</h1>
  </div>
</template>

<style scoped>
.app {
  text-align: center;
  margin-top: 100px;
  font-family: system-ui, sans-serif;
}
</style>
