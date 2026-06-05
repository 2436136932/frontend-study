<!-- <script>
// setup
//1.执行时机，比beforeCreate还要早
//2.setup函数中，获取不到this(this是undefined)
//3.数据 和 函数，需要在 setup最后 return，才能模板中应用
export default {
  setup() {
    // console.log('setup函数',this)
    //数据
    const message = 'hello Vue3'
    //函数
    const logMessage = () => {
      console.log(message)
      }
      return {
        message,
        logMessage
    }
  },
      beforeCreate() {
        console.log('beforeCreate函数')
      }
}
</script>

<template>
  <div>
    <h1>{{ message }}</h1>
    <button @click="logMessage">点击我</button>
  </div>
</template> -->


<script setup>
const message = 'this is a message'
const logMessage = () => {
  console.log(message)
}
</script>

<template>
  <div>{{ message }}</div>
  <button @click="logMessage">按钮</button>
</template>
