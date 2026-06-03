// axios 公共配置
axios.defaults.baseURL = 'http://geek.itheima.net'
axios.defaults.timeout = 5000

// 添加请求拦截器
// 每次发请求之前，都会先经过这里
axios.interceptors.request.use(function (config) {
    // 从本地缓存中取出 token
    const token = localStorage.getItem('token')
    // 如果 token 存在，就把它放到请求头的 Authorization 字段里
    // 格式：Bearer + 空格 + token（后端要求的格式）
    token && (config.headers.Authorization = `Bearer ${token}`)

    // 必须 return config，否则请求发不出去
    return config
}, function (error) {
    // 请求发送失败时走这里
    return Promise.reject(error)
})

// 添加响应拦截器
// 每次请求返回后，都会先经过这里
axios.interceptors.response.use(function (response) {
    // 2xx 范围内的状态码都会触发该函数
    const result = response.data
    // 对响应数据做点什么
    return result
}, function (error) {
    // 超出 2xx 范围的状态码都会触发该函数
    // 对响应错误做点什么，例如：统一对 401 身份验证失败情况做出处理
    console.dir(error)
    if (error?.response?.status === 401) {
        alert('身份验证失败，请重新登录')
        localStorage.clear()
        location.href = '../login/index.html'
    }
    return Promise.reject(error)
})


/*
    ============================================================
    本文件知识点总结
    ============================================================

    一、axios 公共配置（全局默认值）
    ────────────────────────────────
    axios.defaults.baseURL = '基地址'
    axios.defaults.timeout = 毫秒数

    - baseURL：设置后，所有请求的 URL 会自动拼接基地址
      例如：axios.post('/v1_0/authorizations')
      实际发送：http://geek.itheima.net/v1_0/authorizations
    - timeout：请求超时时间，超过这个时间没响应就报错（单位：毫秒）
      5000 = 5秒

    二、请求拦截器（interceptors.request）
    ────────────────────────────────
    作用：在请求发出去之前，先拦截下来，做一些统一处理

    语法：
    axios.interceptors.request.use(成功回调, 失败回调)

    成功回调：function (config) { ... return config }
      - config 是本次请求的配置对象（包含 url、method、headers 等）
      - 可以在这里修改 config，比如给请求头加 token
      - 【必须】return config，否则请求不会发出去

    失败回调：function (error) { ... return Promise.reject(error) }
      - 请求发送失败时触发（比较少见）
      - return Promise.reject(error) 把错误继续传递下去

    三、token 统一携带
    ────────────────────────────────
    为什么要在拦截器里加 token？
      - 登录成功后，后端返回一个 token（身份令牌）
      - 后续调用需要登录才能用的接口时，必须携带 token
      - 如果每个请求都手写 headers，太麻烦
      - 放在拦截器里，所有请求自动带上，只需写一次

    流程：
      1. 登录成功 → localStorage.setItem('token', token)  保存 token
      2. 发任何请求 → 拦截器自动取出 token → 放入请求头
      3. 后端收到请求 → 从 Authorization 头里取出 token → 验证身份

    代码解析：
      const token = localStorage.getItem('token')
      token && (config.headers.Authorization = `Bearer ${token}`)

      - localStorage.getItem('token')：从本地存储取 token
      - token && (...)：短路运算，token 存在才执行后面的赋值
        相当于：if (token) { config.headers.Authorization = ... }
      - `Bearer ${token}`：Bearer 是 token 的认证方式（JWT 标准格式）
        例如：Bearer eyJhbGciOiJIUzI1NiIs...

    四、请求流程图
    ────────────────────────────────
    用户操作（如点击按钮）
        ↓
    axios.post('/v1_0/authorizations', data)
        ↓
    【请求拦截器】← 在这里自动加 token 到请求头
        ↓
    拼接 baseURL → http://geek.itheima.net/v1_0/authorizations
        ↓
    发送请求到服务器
        ↓
    服务器返回响应
        ↓
    【响应拦截器】（如果有的话）
        ↓
    .then(res) 或 try { await } 拿到结果

    五、响应拦截器（interceptors.response）
    ────────────────────────────────
    作用：在请求返回后，先拦截下来，做一些统一处理

    语法：
    axios.interceptors.response.use(成功回调, 失败回调)

    成功回调：function (response) { ... return response }
      - response 是服务器返回的完整响应对象（包含 data、status、headers 等）
      - 可以在这里统一处理响应数据，比如提取 response.data
      - return response 把响应继续传递给 .then()

    失败回调：function (error) { ... return Promise.reject(error) }
      - 状态码不在 2xx 范围内时触发（如 401、403、404、500 等）
      - 可以在这里统一处理错误，比如 401 身份过期自动跳登录页
      - return Promise.reject(error) 把错误继续传递下去，让业务代码也能捕获

    401 身份验证失败处理：
      - 401 = 未授权，token 过期或无效
      - 统一处理：弹出提示 → 清空本地缓存 → 跳转登录页
      - 这样所有接口的 401 错误都会自动跳登录，不用每个请求单独处理

    六、完整请求流程图
    ────────────────────────────────
    用户操作（如点击按钮）
        ↓
    axios.post('/v1_0/authorizations', data)
        ↓
    【请求拦截器】← 在这里自动加 token 到请求头
        ↓
    拼接 baseURL → http://geek.itheima.net/v1_0/authorizations
        ↓
    发送请求到服务器
        ↓
    服务器返回响应
        ↓
    【响应拦截器】← 在这里判断状态码、处理 401 错误
        ↓
    .then(res) 或 try { await } 拿到结果

    七、拦截器对比总结
    ────────────────────────────────
    请求拦截器（request）        |  响应拦截器（response）
    ─────────────────────────────────────────────────────
    在请求发出去之前执行        |  在请求返回后执行
    统一添加 token             |  统一处理 401 错误
    统一添加 loading           |  统一提取 response.data
    统一处理参数               |  统一处理错误提示

    八、相关 API 对比
    ────────────────────────────────
    localStorage.setItem('key', value)  → 存数据（登录成功时存 token）
    localStorage.getItem('key')         → 取数据（拦截器里取 token）
    localStorage.removeItem('key')      → 删数据（退出登录时删 token）
    localStorage.clear()                → 清空所有数据（401 时清空）
    alert('内容')                       → 弹出提示框（身份验证失败时提示）
    location.href = 'url'               → 页面跳转（跳转登录页）
*/
