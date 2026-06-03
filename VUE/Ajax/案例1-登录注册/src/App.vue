<script setup>
import { ref } from 'vue'
import axios from 'axios'

// 接口文档：
// 注册 POST http://hmajax.itheima.net/api/register
// 登录 POST http://hmajax.itheima.net/api/login
// 参数：username（中英文数字，最少8位）、password（最少6位）

// 表单数据
const message = ref('')
const username = ref('')
const password = ref('')
const messageVisible = ref(false)

// 根据提示信息返回不同的 class
const getMessageClass = (msg) => {
  if (!msg) return {}

  // 成功
  if (msg.includes('成功')) return { success: true }

  // 账号/用户名被占用
  if (msg.includes('被占用')) return { warning: true }
  if (msg.includes('已注册')) return { warning: true }
  if (msg.includes('账号已存在')) return { warning: true }
  if (msg.includes('用户名') && msg.includes('存在')) return { warning: true }

  // 用户名/账号不存在
  if (msg.includes('不存在')) return { warning: true }
  if (msg.includes('未注册')) return { warning: true }
  if (msg.includes('未找到')) return { warning: true }

  // 用户名相关错误
  if (msg.includes('用户名') && msg.includes('不能为空')) return { error: true }
  if (msg.includes('用户名') && msg.includes('长度')) return { error: true }
  if (msg.includes('用户名') && msg.includes('格式')) return { error: true }
  if (msg.includes('用户名') && msg.includes('错误')) return { error: true }
  if (msg.includes('用户名') && msg.includes('无效')) return { error: true }
  if (msg.includes('用户名')) return { error: true }

  // 密码相关错误
  if (msg.includes('密码') && msg.includes('不能为空')) return { error: true }
  if (msg.includes('密码') && msg.includes('长度')) return { error: true }
  if (msg.includes('密码') && msg.includes('格式')) return { error: true }
  if (msg.includes('密码') && msg.includes('错误')) return { error: true }
  if (msg.includes('密码') && msg.includes('不正确')) return { error: true }
  if (msg.includes('密码')) return { error: true }

  // 通用失败
  if (msg.includes('失败')) return { error: true }
  if (msg.includes('错误')) return { error: true }
  if (msg.includes('异常')) return { error: true }
  if (msg.includes('网络')) return { error: true }

  // 其它
  return { info: true }
}

// 显示提示信息
const showMessage = (text) => {
  message.value = text
  messageVisible.value = true

  // 1.6秒后开始淡出
  setTimeout(() => {
    messageVisible.value = false
  }, 1600)

  // 2秒后（淡出动画结束）再清空文字
  setTimeout(() => {
    message.value = ''
  }, 2000)
}

// 注册
const register = async () => {
  try {
    const res = await axios.post('http://hmajax.itheima.net/api/register', {
      username: username.value,
      password: password.value
    })
    username.value = ''
    password.value = ''
    showMessage(res.data.message)
  } catch (err) {
    showMessage(err.response.data.message)
  }
}

// 登录
const login = async () => {
  try {
    const res = await axios.post('http://hmajax.itheima.net/api/login', {
      username: username.value,
      password: password.value
    })
    showMessage(res.data.message)
  } catch (err) {
    showMessage(err.response.data.message)
  }
}
</script>

<template>
  <div class="login-box">
    <h2>登录 / 注册</h2>

    <div class="form-message" :class="[getMessageClass(message), { active: messageVisible }]">{{ message }}</div>

    <div class="form-item">
      <label>用户名</label>
      <input type="text" v-model="username" placeholder="请输入用户名（≥8位）">
    </div>

    <div class="form-item">
      <label>密码</label>
      <input type="password" v-model="password" placeholder="请输入密码（≥6位）">
    </div>

    <div class="btns">
      <button class="btn-register" @click="register">注册</button>
      <button class="btn-login" @click="login">登录</button>
    </div>
  </div>
</template>

<style scoped>
.login-box {
  width: 360px;
  margin: 80px auto;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  font-family: system-ui, sans-serif;
}

.login-box h2 {
  text-align: center;
  margin: 0 0 24px;
  color: #333;
}

.form-message {
  width: 100%;
  margin-bottom: 18px;
  font-size: 14px;
  text-align: center;
  line-height: 1.5;
  box-sizing: border-box;
  min-height: 44px;
  max-height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 16px;
  opacity: 0;
  transform: translateY(-4px);
  transition: all .5s ease-in-out;
  border: 1px solid transparent;
  border-radius: 6px;
  background: transparent;
  color: transparent;
  overflow: hidden;
  pointer-events: none;
}

.form-message.active {
  opacity: 1;
  transform: translateY(0);
}

.form-message.success {
  background: #f0f9eb;
  border: 1px solid #e1f3d8;
  border-radius: 6px;
  padding: 12px 16px;
  color: #67c23a;
  font-weight: 500;
  opacity: 0.8;
}

.form-message.error {
  background: #fef0f0;
  border: 1px solid #fde2e2;
  border-radius: 6px;
  padding: 12px 16px;
  color: #f56c6c;
  font-weight: 500;
  opacity: 0.8;
}

.form-message.warning {
  background: #fdf6ec;
  border: 1px solid #faecd8;
  border-radius: 6px;
  padding: 12px 16px;
  color: #e6a23c;
  font-weight: 500;
  opacity: 0.8; 
}

.form-message.info {
  background: #f4f4f5;
  border: 1px solid #e9e9eb;
  border-radius: 6px;
  padding: 12px 16px;
  color: #909399;
  font-weight: 500;
  opacity: 0.8; 
}

.form-item {
  margin-bottom: 18px;
}

.form-item label {
  display: block;
  margin-bottom: 6px;
  font-size: 14px;
  color: #666;
}

.form-item input {
  width: 100%;
  height: 38px;
  padding: 0 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  outline: none;
  box-sizing: border-box;
}

.form-item input:focus {
  border-color: #409eff;
}

.btns {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

.btns button {
  flex: 1;
  height: 40px;
  border: none;
  border-radius: 6px;
  font-size: 15px;
  cursor: pointer;
  transition: opacity 0.2s;
}

.btns button:hover {
  opacity: 0.85;
}

.btn-register {
  background: #f0f0f0;
  color: #333;
}

.btn-login {
  background: #409eff;
  color: #fff;
}
</style>
