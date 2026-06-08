# Pinia 组合式写法学习笔记

这份文档基于你当前项目 `vue3-pinia-demo` 的实际代码来讲解 **Pinia 的组合式写法（Setup Store）**。

你现在已经把项目里的 Store 改成了 Vue3 更主流的组合式风格，所以这份文档会重点讲：

- 为什么 Vue3 更常用组合式
- Pinia 的 Setup Store 怎么写
- `ref / computed / async` 在 Store 里怎么用
- 组件里怎么使用组合式 Store
- 和之前的 `state / getters / actions` 写法有什么区别

---

## 1. 为什么现在更推荐组合式写法

Vue3 的主流开发方式就是组合式 API，也就是你熟悉的这些：

- `ref`
- `reactive`
- `computed`
- `watch`
- `script setup`

例如在组件中你会这样写：

```vue
<script setup>
import { computed, ref } from 'vue'

const count = ref(0)
const doubleCount = computed(() => count.value * 2)

const increment = () => {
  count.value++
}
</script>
```

Pinia 也支持这种风格，所以在实际开发里，很多 Vue3 项目会更喜欢用 **Setup Store**。

这样做的好处是：

- 写法和组件中的组合式 API 完全统一
- 更容易复用逻辑
- 更适合复杂业务
- 更符合 Vue3 的整体思路

---

## 2. 组合式 Pinia 的核心写法

Pinia 的组合式写法长这样：

```js
export const useXxxStore = defineStore('storeId', () => {
  const xxx = ref(...)
  const yyy = computed(...)

  const fn = () => {
    ...
  }

  return {
    xxx,
    yyy,
    fn,
  }
})
```

### 你要记住的关键点

#### 1）第二个参数不是对象，而是函数

以前你学的可能是：

```js
defineStore('counter', {
  state: ...,
  getters: ...,
  actions: ...,
})
```

那是 **Option Store**。

现在你改成的是：

```js
defineStore('counter', () => {
  ...
})
```

这就是 **Setup Store**。

#### 2）状态自己用 `ref` 或 `reactive` 定义

不再写：

```js
state: () => ({ ... })
```

而是写：

```js
const count = ref(0)
```

#### 3）计算属性自己用 `computed`

不再写：

```js
getters: {
  doubleCount: ...
}
```

而是写：

```js
const doubleCount = computed(() => count.value * 2)
```

#### 4）方法自己定义函数

不再写：

```js
actions: {
  increment() {}
}
```

而是写：

```js
const increment = () => {
  count.value++
}
```

#### 5）最后必须 `return`

只有 `return` 出去的内容，组件里才能访问。

---

## 3. 你的项目里 Pinia 仍然是一样注册的

文件位置： [main.js](file:///G:/前端学习/VUE/vue3-pinia-demo/src/main.js#L1-L10)

```js
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import './style.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.mount('#app')
```

这里和组合式、选项式没有关系。

Pinia 注册方式永远都是：

1. `createPinia()` 创建实例
2. `app.use(pinia)` 挂载到应用

---

## 4. 计数器 Store 的组合式写法

文件位置： [counter.js](file:///G:/前端学习/VUE/vue3-pinia-demo/src/stores/counter.js#L1-L28)

```js
import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', () => {
  const count = ref(0)

  const doubleCount = computed(() => count.value * 2)

  const increment = () => {
    count.value++
  }

  const decrement = () => {
    count.value--
  }

  const reset = () => {
    count.value = 0
  }

  return {
    count,
    doubleCount,
    increment,
    decrement,
    reset,
  }
})
```

---

## 5. 在组合式 Store 中如何理解数据和方法

### 1）`count`

```js
const count = ref(0)
```

这是响应式状态。

作用：

- 保存计数器当前值
- 初始值是 `0`

这里用的是 `ref`，因为它是一个基础类型数字。

### 2）`doubleCount`

```js
const doubleCount = computed(() => count.value * 2)
```

这是计算属性。

作用：

- 根据 `count` 自动计算出两倍值

如果：

- `count.value = 2`

那么：

- `doubleCount.value = 4`

### 3）`increment`

```js
const increment = () => {
  count.value++
}
```

这是方法。

作用：

- 点击按钮时让数字加 1

### 4）为什么这里要写 `.value`

因为在 **Store 内部** 你操作的是 `ref` 本身。

例如：

```js
count.value++
```

这是组合式 API 的正常写法。

但在组件外部拿到 Store 后，Pinia 会帮你自动解包，所以模板里通常不需要写 `.value`。

这个区别非常重要。

---

## 6. 组合式 Store 的返回值为什么重要

在 Setup Store 里：

```js
return {
  count,
  doubleCount,
  increment,
  decrement,
  reset,
}
```

只有这里 return 出去的属性和方法，组件中才能使用。

如果你定义了：

```js
const test = ref('123')
```

但是没有 return：

```js
return {
  count,
}
```

那么组件里就访问不到 `test`。

所以你可以把 `return` 理解成：

- “把 Store 中要暴露出去的内容导出给组件使用”

---

## 7. 用户 Store 的组合式写法

文件位置： [user.js](file:///G:/前端学习/VUE/vue3-pinia-demo/src/stores/user.js#L1-L50)

```js
import axios from 'axios'
import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', () => {
  const name = ref('默认用户')
  const age = ref(18)
  const channelList = ref([])
  const loading = ref(false)
  const error = ref('')

  const description = computed(() => `${name.value}，${age.value} 岁`)
  const channelCount = computed(() => channelList.value.length)

  const updateName = (newName) => {
    name.value = newName
  }

  const fetchChannels = async () => {
    loading.value = true
    error.value = ''

    try {
      const res = await axios.get('/api/v1_0/channels')
      channelList.value = res.data.data.channels
    } catch (err) {
      error.value = '获取频道列表失败，请检查代理配置或接口状态'
      channelList.value = []
    } finally {
      loading.value = false
    }
  }

  const growUp = () => {
    age.value++
  }

  return {
    name,
    age,
    channelList,
    loading,
    error,
    description,
    channelCount,
    updateName,
    fetchChannels,
    growUp,
  }
})
```

---

## 8. 这个 user store 里都学到了什么

这个 Store 基本把组合式 Pinia 的基础内容都串起来了。

### 状态部分

```js
const name = ref('默认用户')
const age = ref(18)
const channelList = ref([])
const loading = ref(false)
const error = ref('')
```

分别表示：

- `name`：用户名
- `age`：年龄
- `channelList`：接口返回的频道列表
- `loading`：是否正在请求中
- `error`：错误信息

### 计算属性部分

```js
const description = computed(() => `${name.value}，${age.value} 岁`)
const channelCount = computed(() => channelList.value.length)
```

作用：

- `description`：把姓名和年龄拼成一句描述
- `channelCount`：统计频道总数

### 方法部分

```js
const updateName = (newName) => {
  name.value = newName
}
```

作用：

- 更新用户名

```js
const growUp = () => {
  age.value++
}
```

作用：

- 年龄加 1

### 异步请求部分

```js
const fetchChannels = async () => {
  loading.value = true
  error.value = ''

  try {
    const res = await axios.get('/api/v1_0/channels')
    channelList.value = res.data.data.channels
  } catch (err) {
    error.value = '获取频道列表失败，请检查代理配置或接口状态'
    channelList.value = []
  } finally {
    loading.value = false
  }
}
```

这是一段很标准的组合式异步逻辑。

---

## 9. 组合式 Pinia 中如何写异步请求

这是你现在最值得重点掌握的一块。

### 标准思路

通常可以按这个流程写：

1. 开启 `loading`
2. 清空旧错误
3. 发送请求
4. 成功时更新数据
5. 失败时记录错误
6. 最后关闭 `loading`

### 你当前项目示例

文件位置： [fetchChannels](file:///G:/前端学习/VUE/vue3-pinia-demo/src/stores/user.js#L18-L31)

```js
const fetchChannels = async () => {
  loading.value = true
  error.value = ''

  try {
    const res = await axios.get('/api/v1_0/channels')
    channelList.value = res.data.data.channels
  } catch (err) {
    error.value = '获取频道列表失败，请检查代理配置或接口状态'
    channelList.value = []
  } finally {
    loading.value = false
  }
}
```

### 这里每一步的含义

#### `loading.value = true`
告诉页面：

- 现在开始加载了

#### `error.value = ''`
告诉页面：

- 开始新请求前，先清空旧错误

#### `await axios.get(...)`
发送异步请求。

#### `channelList.value = res.data.data.channels`
把接口返回的频道数组保存到状态中。

#### `catch`
如果接口失败：

- 给出错误提示
- 清空旧数据

#### `finally`
不管成功失败都执行，用来收尾最合适。

---

## 10. 组件中如何使用组合式 Store

文件位置： [App.vue](file:///G:/前端学习/VUE/vue3-pinia-demo/src/App.vue#L1-L6)

```js
<script setup>
import { useCounterStore } from './stores/counter'
import { useUserStore } from './stores/user'

const counterStore = useCounterStore()
const userStore = useUserStore()
</script>
```

### 三步走

#### 第一步：导入

```js
import { useCounterStore } from './stores/counter'
```

#### 第二步：调用

```js
const counterStore = useCounterStore()
```

#### 第三步：使用

```js
counterStore.count
counterStore.doubleCount
counterStore.increment()
```

这个过程和 Option Store 一样，区别主要在 **Store 内部的定义方式**。

---

## 11. 为什么组件里不用写 `.value`

这是组合式 Pinia 里最容易让人糊涂的点。

### 在 Store 内部
你定义的是 `ref`：

```js
const count = ref(0)
```

所以你修改它时要写：

```js
count.value++
```

### 在组件里
你通过 `useCounterStore()` 拿到的是 Store 实例。

Pinia 会帮你把返回的 `ref` 自动解包，所以你可以直接写：

```js
counterStore.count
counterStore.doubleCount
userStore.name
```

模板里也是直接写：

```html
<p>{{ counterStore.count }}</p>
<p>{{ userStore.name }}</p>
```

### 简单记忆

- **Store 内部操作 ref：要写 `.value`**
- **组件里通过 Store 使用：通常不用 `.value`**

---

## 12. 页面模板中如何使用组合式 Store

文件位置： [App.vue](file:///G:/前端学习/VUE/vue3-pinia-demo/src/App.vue#L8-L63)

### 显示计数器数据

```html
<p class="count">Count: {{ counterStore.count }}</p>
<p class="double">Double: {{ counterStore.doubleCount }}</p>
```

### 调用计数器方法

```html
<button @click="counterStore.increment">+1</button>
<button @click="counterStore.decrement">-1</button>
<button @click="counterStore.reset">重置</button>
```

### 显示用户信息

```html
<p>姓名：{{ userStore.name }}</p>
<p>年龄：{{ userStore.age }}</p>
<p>描述：{{ userStore.description }}</p>
```

### 调用用户方法

```html
<button @click="userStore.updateName('张三')">改名张三</button>
<button @click="userStore.updateName('李四')">改名李四</button>
<button @click="userStore.growUp()">+1 岁</button>
```

### 渲染接口列表

```html
<p>频道数量：{{ userStore.channelCount }}</p>
<button @click="userStore.fetchChannels()">获取频道列表</button>

<ul v-if="userStore.channelList.length" class="channel-list">
  <li v-for="item in userStore.channelList" :key="item.id">
    {{ item.id }} - {{ item.name }}
  </li>
</ul>
```

---

## 13. 组合式写法和之前选项式写法的区别

这是你现在最应该建立起来的对照关系。

### 以前的 Option Store

```js
defineStore('counter', {
  state: () => ({
    count: 0,
  }),
  getters: {
    doubleCount: (state) => state.count * 2,
  },
  actions: {
    increment() {
      this.count++
    },
  },
})
```

### 现在的 Setup Store

```js
defineStore('counter', () => {
  const count = ref(0)
  const doubleCount = computed(() => count.value * 2)

  const increment = () => {
    count.value++
  }

  return {
    count,
    doubleCount,
    increment,
  }
})
```

### 对照理解

| 选项式写法 | 组合式写法 |
| --- | --- |
| `state` | `ref / reactive` |
| `getters` | `computed` |
| `actions` | 普通函数 / 箭头函数 |
| `this.count` | `count.value` |
| 自动按对象分类 | 自己组织逻辑并 return |

---

## 14. 为什么你之前那句 `const state = ref(0)` 容易出错

你之前写的是：

```js
const state = ref(0)
```

这句本身不一定错，问题在于：

- 如果你整个 Store 还是 `state / getters / actions` 的对象写法
- 那你就把两套风格混在一起了

### 错误混搭示意

```js
defineStore('counter', {
  const state = ref(0)
  getters: { ... },
  actions: { ... },
})
```

这是不成立的。

### 正确组合式思路

```js
defineStore('counter', () => {
  const count = ref(0)

  return {
    count,
  }
})
```

### 另外命名也更推荐 `count`

不建议：

```js
const state = ref(0)
```

更推荐：

```js
const count = ref(0)
```

因为它能直接表达这份数据的业务含义。

---

## 15. 组合式 Pinia 中 `storeToRefs` 还要不要用

要，仍然经常会用。

比如你想解构 Store：

```js
const counterStore = useCounterStore()
```

如果你直接写：

```js
const { count, doubleCount } = counterStore
```

有时会丢失响应式或造成理解混乱。

更稳妥的方式是：

```js
import { storeToRefs } from 'pinia'

const counterStore = useCounterStore()
const { count, doubleCount } = storeToRefs(counterStore)
const { increment, decrement } = counterStore
```

### 记忆方式

- 状态和计算属性：用 `storeToRefs`
- 方法：直接解构

---

## 16. 组合式写法的优点

你现在改成组合式后，会更容易接上 Vue3 的主流思路。

### 优点 1：和组件写法统一

组件里用：

- `ref`
- `computed`
- `watch`

Store 里也用：

- `ref`
- `computed`
- `watch`

这样学习成本更低。

### 优点 2：逻辑更灵活

你可以按功能组织代码，而不是被 `state / getters / actions` 三个区域固定住。

### 优点 3：更适合复杂逻辑

如果以后你在 Store 中要写：

- `watch`
- 组合式函数复用
- 更复杂的数据联动

组合式写法通常更顺手。

---

## 17. 你当前项目已经覆盖的组合式知识点

现在这个项目已经包含了这些非常实用的基础内容：

- Pinia 注册
- Setup Store 写法
- `ref` 定义状态
- `computed` 定义派生数据
- 普通函数定义操作方法
- 组件中调用 Store
- 异步请求写进 Store
- `loading / error` 状态管理
- 模板渲染接口列表
- 代理接口请求

对入门来说，这已经是一套很完整的组合式 Pinia 练习项目。

---

## 18. 常见错误总结

### 1）忘记 return

组合式 Store 中最常见错误之一就是忘记 return：

```js
defineStore('counter', () => {
  const count = ref(0)
})
```

这样组件里拿不到 `count`。

### 2）在 Store 内部忘写 `.value`

错误：

```js
count++
```

正确：

```js
count.value++
```

因为 `count` 是 `ref`。

### 3）组件中又多写 `.value`

错误：

```js
counterStore.count.value
```

一般情况下，正确是：

```js
counterStore.count
```

### 4）把选项式和组合式混着写

错误示意：

```js
defineStore('counter', {
  state: () => ({ count: 0 }),
  const num = ref(0)
})
```

必须二选一：

- 要么用 Option Store
- 要么用 Setup Store

### 5）接口错误不处理

如果只写：

```js
const res = await axios.get(...)
channelList.value = res.data.data.channels
```

一旦失败，页面体验就会很差。

更规范的做法是你现在项目里的：

- `loading`
- `error`
- `try / catch / finally`

---

## 19. 你现在最推荐的学习顺序

建议你按下面顺序继续练：

### 第一步：彻底看懂 counter store
文件： [counter.js](file:///G:/前端学习/VUE/vue3-pinia-demo/src/stores/counter.js)

重点理解：

- `ref`
- `computed`
- return
- `count.value` 和 `counterStore.count` 的区别

### 第二步：看懂 user store
文件： [user.js](file:///G:/前端学习/VUE/vue3-pinia-demo/src/stores/user.js)

重点理解：

- 多个 `ref` 状态
- 异步方法
- `loading` 和 `error`
- 接口数据保存到 Store

### 第三步：回到页面看如何使用
文件： [App.vue](file:///G:/前端学习/VUE/vue3-pinia-demo/src/App.vue)

重点理解：

- 获取 Store 实例
- 模板直接渲染数据
- 点击按钮调用方法
- `v-for` 渲染列表

---

## 20. 一句话总结

Pinia 组合式写法可以这样记：

- **用 `ref` 存状态**
- **用 `computed` 做派生数据**
- **用普通函数写业务逻辑**
- **最后通过 `return` 暴露给组件使用**

如果你把这四句话真正理解了，Pinia 的组合式基础就已经掌握了。

---

## 21. 对照你当前项目的学习入口

建议你边看文档边对照代码：

- Pinia 注册： [main.js](file:///G:/前端学习/VUE/vue3-pinia-demo/src/main.js#L1-L10)
- 组合式计数器 Store： [counter.js](file:///G:/前端学习/VUE/vue3-pinia-demo/src/stores/counter.js)
- 组合式用户 Store： [user.js](file:///G:/前端学习/VUE/vue3-pinia-demo/src/stores/user.js)
- 页面使用： [App.vue](file:///G:/前端学习/VUE/vue3-pinia-demo/src/App.vue)

最好的学习方法还是这四步：

1. 看文档
2. 对照代码
3. 自己手改
4. 看页面效果

这样学 Pinia 会非常快。
