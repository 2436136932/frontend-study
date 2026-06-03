/**
 * 目标1：验证码登录
 * 1.1 在 utils/request.js 配置 axios 请求基地址
 * 1.2 收集手机号和验证码数据
 * 1.3 基于 axios 调用验证码登录接口
 * 1.4 使用 Bootstrap 的 Alert 警告框反馈结果给用户
 */

// 1.2 收集手机号和验证码数据
// 点击登录按钮时触发
// 回调函数加 async，这样里面就可以用 await
document.querySelector('.btn').addEventListener('click', async (e) => {
    // 阻止表单默认提交行为（防止页面刷新）
    e.preventDefault()

    // 获取表单 DOM 元素
    const form = document.querySelector('.login-form')

    // 用 serialize 把表单数据序列化成对象
    // hash: true → 返回对象格式 { phone: '13800138000', code: '246810' }
    // empty: true → 即使输入框为空也会收集（值为空字符串）
    const data = serialize(form, { hash: true, empty: true })
    console.log(data)

    // 1.3 基于 axios 调用验证码登录接口
    // 用 try-catch 包裹 await，捕获请求失败的错误
    try {
        // await 等待 POST 请求完成，结果直接赋值给 res
        // 等价于：axios.post(...).then(res => { ... })
        const res = await axios.post('/v1_0/authorizations', data)
        myAlert(true, '登录成功')
        // 登录成功后，将 token 令牌字符串保存到本地缓存
        localStorage.setItem('token', res.data.token)
        // 登录成功后，跳转到首页
        setTimeout(() => {
            window.location.href = '../content/index.html'
        }, 1500)
        console.log(res)
    } catch (err) {
        // 请求失败走这里（网络错误、状态码非 2xx 等）
        // 等价于：.catch(err => { ... })
        myAlert(false, err.response.data.message)
        console.log(err)
    }
})
