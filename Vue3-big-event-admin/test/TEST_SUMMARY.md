# 大事件管理系统 Pytest 自动化测试总结报告

## 一、报告信息

- 测试项目：Vue3 大事件管理系统
- 前端项目：`G:\前端学习\Vue3-big-event-admin`
- Pytest 项目：`G:\前端学习\Vue3-big-event-admin\test`
- 后端地址：`https://big-event-vue-api-t.itheima.net`
- Python：3.13.2
- Pytest：9.0.2
- 执行日期：2026-07-13
- 最终结果：**29 passed，0 failed，0 skipped**
- 执行耗时：**12.54 秒**

## 二、实现结果

测试项目已从单个 400 多行文件拆分为：

```text
test/
├── pytest.ini
├── requirements.txt
├── README_PYTEST.md
├── TEST_SUMMARY.md
├── reports/
│   └── test-report.html
└── tests/
    ├── conftest.py
    ├── test_api_basics.py
    ├── test_user.py
    ├── test_category.py
    └── test_article.py
```

### 各模块结果

| 模块 | 用例数 | 结果 |
|---|---:|---|
| 服务器、登录、token 权限 | 7 | 7 passed |
| 文章列表、筛选、详情、编辑 | 10 | 10 passed |
| 分类列表、创建、详情、编辑、校验 | 8 | 8 passed |
| 用户信息与写接口权限保护 | 4 | 4 passed |
| 合计 | 29 | 29 passed |

## 三、测试覆盖

### 1. 基础与登录

验证内容：

- API 服务器可达，根地址返回 401，说明服务在线并要求认证。
- 正确账号密码登录成功。
- 登录响应包含非空 token。
- 空用户名、空密码、非法/不存在用户名被拒绝。
- 无 token 访问保护接口返回 401。
- 伪造 token 访问保护接口返回 401。

### 2. 用户模块

验证内容：

- `GET /my/userinfo` 返回当前账号信息。
- 用户对象包含 `id`、`username`、`nickname`、`email`、`user_pic`。
- ID 是正整数，用户名、昵称、邮箱类型正确。
- 未认证时，修改资料、修改头像、修改密码接口全部返回 401。

出于真实账号安全考虑，未执行以下成功写操作：

- 修改昵称和邮箱。
- 修改头像。
- 修改密码。

这些流程会永久改变真实账号状态，必须使用可重置的专用测试账号后再启用。

### 3. 分类模块

验证内容：

- 分类列表返回数组。
- 每个分类包含 `id`、`cate_name`、`cate_alias`。
- ID、名称、别名类型正确。
- fixture 创建的分类可以按 ID 查询详情。
- fixture 创建的分类可以编辑并验证新值。
- 空名称、空别名、超长名称、非法别名被拒绝。
- 不存在的分类 ID 返回业务失败。

后端实际规则：

- `cate_name` 不能为空。
- `cate_name` 长度不能超过 10。
- `cate_alias` 不能为空。
- `cate_alias` 只能包含字母和数字。

### 4. 文章模块

验证内容：

- `pagesize=1/2/5` 时，返回条数不超过指定值。
- 文章列表 `total` 是整数，`data` 是数组。
- 按“已发布”和“草稿”筛选时，返回项状态均匹配筛选值。
- 文章列表项包含前端表格需要的字段。
- 自动创建的草稿文章可以查询完整详情。
- 自动创建的文章可以编辑标题、内容和状态。
- 缺少标题时发布被拒绝。
- 不存在的文章 ID 返回业务失败。

文章发布和编辑使用 `multipart/form-data`，测试通过 `files={...}` 模拟 Vue 中的 `FormData` 和封面 File 对象。

## 四、Fixture 与自动清理

### 登录 fixture

`logged_in_session` 使用 session 作用域：

- 整次 pytest 只登录一次。
- 复用 `requests.Session` 连接池。
- 后续请求自动携带 Authorization。
- 不打印完整 token。

### 分类 fixture

`created_category` 的执行顺序：

1. 生成唯一名称和别名。
2. 新增分类。
3. 查询列表获取精确 ID。
4. `yield` 给测试函数。
5. 测试结束后在 `finally` 中删除该 ID。

### 文章 fixture

`created_article` 的执行顺序：

1. 依赖 `created_category` 创建专属分类。
2. 使用内存 JPEG 发布草稿文章。
3. 分页查找新文章 ID。
4. `yield` 给测试函数。
5. 测试结束后先删除文章。
6. 再由分类 fixture 删除分类。

本次最终执行日志确认每个测试资源均执行了自动清理。

## 五、清理核验

全套测试结束后，对本轮创建的资源进行独立查询：

### 文章

- ID 22443：`没有查到对应的数据！`
- ID 22444：`没有查到对应的数据！`

### 分类

- ID 22496：`获取文章分类失败！`
- ID 22497：`获取文章分类失败！`
- ID 22498：`获取文章分类失败！`
- ID 22499：`获取文章分类失败！`
- ID 22500：`获取文章分类失败！`

结论：**本轮创建的 2 篇测试文章与 5 个测试分类均已删除，没有遗留测试数据。**

## 六、发现与说明

### 1. WAF 会拦截非浏览器请求

请求缺少浏览器 User-Agent、Origin、Referer 时，云端网关可能返回 405 HTML 页面，而不是应用预期的 401 JSON。

测试已统一使用浏览器请求头，确保请求到达应用 API。修正后，用户写接口的无认证请求都稳定返回 401。

### 2. HTTP 成功不等于业务成功

该后端常在参数错误时返回 HTTP 200，同时响应：

```json
{
  "code": 2,
  "message": "校验错误"
}
```

所以测试同时检查：

```python
assert response.status_code == 200
assert data["code"] == 0
```

### 3. 筛选空结果不能证明完整业务

当前账号没有草稿时，`state=草稿` 返回空数组。这个结果符合接口合同，但空数组会让逐项状态检查自然通过。

为提高验证强度，文章 fixture 会先创建一篇草稿，再验证详情和编辑流程。未来还可添加“创建草稿后按草稿筛选，必须找到该 ID”的专门场景。

### 4. 真实账号曾有历史测试数据

账号文章列表包含之前生成的 Pytest 测试文章。当前实现不会删除这些历史数据，因为无法确认它们是否仍需要保留；自动清理只针对本轮精确捕获的 ID。

## 七、生成文件

- 详细学习教程：`README_PYTEST.md`
- 本总结报告：`TEST_SUMMARY.md`
- HTML 测试报告：`reports/test-report.html`
- 公共 fixtures：`tests/conftest.py`
- 基础测试：`tests/test_api_basics.py`
- 用户测试：`tests/test_user.py`
- 分类测试：`tests/test_category.py`
- 文章测试：`tests/test_article.py`

## 八、运行命令

```powershell
cd "G:\前端学习\Vue3-big-event-admin\test"

# 安装依赖
pip install -r requirements.txt

# 全部测试并显示 print
pytest -v -s

# 只读/异常测试，不执行分类文章写操作
pytest -m "not write" -v -s

# 分类模块
pytest -m category -v -s

# 文章模块
pytest -m article -v -s

# 只执行自动清理的写测试
pytest -m write -v -s

# 只跑上次失败
pytest --lf -v -s

# 生成自包含 HTML 报告
pytest -v --html=reports/test-report.html --self-contained-html
```

## 九、环境变量配置

```powershell
$env:BIG_EVENT_BASE_URL = "https://big-event-vue-api-t.itheima.net"
$env:BIG_EVENT_USERNAME = "专用测试账号"
$env:BIG_EVENT_PASSWORD = "专用测试密码"
$env:BIG_EVENT_TIMEOUT = "15"
pytest -v -s
```

团队项目或 CI 中应使用环境变量/密钥管理，不应把真实密码提交到 Git。

## 十、后续建议

1. 准备可重置的独立测试账号，补齐用户资料、头像、密码的成功写流程。
2. 增加 `requests-mock` 或 `responses`，测试超时、断网、500、非 JSON 响应。
3. 使用 Playwright 测 Vue 页面的登录、筛选、添加、编辑、删除操作。
4. 将 HTML/JUnit 报告接入 GitHub Actions 或 Jenkins。
5. 给测试账号数据增加定期清理任务，清除早期遗留的 Pytest 测试文章。

## 十一、最终结论

当前测试套件已覆盖大事件管理系统的主要 API 合同、登录与权限控制、分类 CRUD、文章分页筛选与安全 CRUD。最终 **29 条用例全部通过**，且本次创建的数据全部清理。测试结构已具备继续扩展到 CI、浏览器 E2E 和专用测试账号写流程的基础。
