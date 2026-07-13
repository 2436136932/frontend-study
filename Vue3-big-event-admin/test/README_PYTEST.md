# 大事件管理系统 Pytest 学习与测试总报告

本文档对应 `G:\前端学习\Vue3-big-event-admin\test` 中的测试项目。目标不是只得到一批通过的测试，而是理解如何根据 Vue 前端代码推导 API 测试、如何组织 pytest 项目，以及如何安全地测试真实后端。

## 1. 项目结构

```text
test/
├── pytest.ini
├── requirements.txt
├── reports/
└── tests/
    ├── conftest.py
    ├── test_api_basics.py
    ├── test_user.py
    ├── test_category.py
    └── test_article.py
```

- `pytest.ini`：pytest 的发现规则、默认参数、自定义标记。
- `requirements.txt`：pytest、requests 和 HTML 报告插件。
- `conftest.py`：所有测试文件自动共享的工具函数和 fixtures。
- `test_api_basics.py`：服务器、登录、缺少/伪造 token。
- `test_user.py`：当前用户信息结构和用户写接口认证保护。
- `test_category.py`：分类列表、非法参数、创建、详情、编辑和清理。
- `test_article.py`：文章分页、筛选、详情、multipart 发布、编辑和清理。

## 2. 从 Vue 代码推导测试

前端 `src/api/user.js` 和 `src/api/article.js` 声明了请求方法、路径和参数；`src/utils/request.js` 声明了基础地址、token 请求头以及业务成功规则 `code === 0`。

因此测试需要同时验证两层结果：

```python
assert response.status_code == 200  # HTTP 层
assert data["code"] == 0            # 业务层
```

HTTP 200 只说明后端成功处理了请求，不代表登录、创建或修改业务一定成功。

## 3. 核心辅助函数

### `api_url(path)`

把 `/api/login` 等相对路径拼成完整 URL。统一封装后，切换测试环境只需要修改 `BIG_EVENT_BASE_URL`。

### `assert_http_ok(response)`

统一检查 HTTP 200 并解析 JSON。失败时会打印状态码和部分响应体，比单独写 `assert status_code == 200` 更容易定位问题。

### `find_category()` 和 `find_article()`

新增接口没有返回新数据 ID，因此创建后需要查询列表，按本轮生成的唯一名称找到 ID。文章查询支持翻页，避免测试数据不在第一页。

## 4. Fixture

### 普通 fixture

```python
@pytest.fixture(scope="session")
def logged_in_session(http_session):
    # 登录
    yield http_session
    # 清除本地 Authorization
```

测试函数只需声明参数：

```python
def test_current_user_schema(logged_in_session):
    ...
```

pytest 会按参数名自动找到并执行 fixture。

### Fixture scope

- `function`：默认，每条测试执行一次。
- `module`：一个测试文件执行一次。
- `session`：整次 pytest 运行只执行一次。

HTTP 连接和登录使用 `session`，减少重复连接和登录请求。

### `yield fixture` 自动清理

```python
@pytest.fixture
def created_category(logged_in_session):
    category = create_category()
    try:
        yield category
    finally:
        delete_category(category["id"])
```

顺序是：

1. `yield` 前创建测试数据。
2. `yield category` 把数据传给测试。
3. 测试执行。
4. 无论测试通过还是失败，`finally` 都尝试清理。

分类和文章写测试只操作本轮创建、带唯一标记的数据，不会删除账号已有数据。

## 5. 参数化

```python
@pytest.mark.parametrize("page_size", [1, 2, 5])
def test_article_list_pagination(logged_in_session, page_size):
    ...
```

一个函数生成三条独立用例。测试逻辑相同、输入数据不同时，应优先用参数化，避免复制粘贴。

分页断言使用：

```python
assert len(articles) <= page_size
```

不能使用 `==`，因为总数据不足时，后端合理地返回少于 `page_size` 条。

## 6. 列表与数据结构断言

```python
assert isinstance(categories, list)
assert {"id", "cate_name", "cate_alias"}.issubset(category)
```

第一句验证 API 返回数组；第二句验证数组中的对象包含前端所依赖的字段。对应 JavaScript：

```javascript
Array.isArray(categories)
```

测试不只是判断接口是否在线，还要保护前后端数据合同。

## 7. 查询参数、JSON 与 Multipart

### GET 查询参数

```python
requests.get(url, params={"pagenum": 1, "pagesize": 5})
```

生成 `?pagenum=1&pagesize=5`，对应 Axios 的 `{ params }`。

### JSON 请求体

```python
requests.post(url, json={"cate_name": name, "cate_alias": alias})
```

用于登录、分类新增和分类编辑。

### Multipart/FormData

```python
requests.post(
    url,
    data={"title": title, "cate_id": category_id},
    files={"cover_img": ("cover.jpg", image, "image/jpeg")},
)
```

文章发布必须包含封面文件，对应 Vue 中的 `new FormData()`。仅使用 `data=` 会发送 `application/x-www-form-urlencoded`，后端无法按文章上传接口解析。

## 8. 安全策略

- 不测试真实账号密码修改成功流程，因为它会改变登录凭证。
- 不修改真实昵称、邮箱或头像。
- 无 token 与伪造 token 测试验证权限保护。
- 分类/文章写测试使用唯一后缀，并自动删除。
- 不删除列表里原有的第一条数据。
- 不打印完整 token。

要覆盖用户资料和密码成功写流程，应准备可随时重置的专用测试账号或本地后端数据库。

## 9. 常用命令

在 `G:\前端学习\Vue3-big-event-admin\test` 中执行：

```powershell
# 全部测试
pytest -v -s

# 只跑基础冒烟
pytest -m smoke -v -s

# 只跑用户模块
pytest -m user -v -s

# 只跑分类模块
pytest -m category -v -s

# 只跑文章模块
pytest -m article -v -s

# 只跑会写入并自动清理数据的用例
pytest -m write -v -s

# 排除写操作，只跑只读/异常测试
pytest -m "not write" -v -s

# 按名称筛选
pytest -k "login" -v -s

# 只跑上次失败
pytest --lf -v -s

# 生成 HTML 报告
pytest -v --html=reports/test-report.html --self-contained-html
```

## 10. 环境变量

默认配置可被覆盖：

```powershell
$env:BIG_EVENT_BASE_URL = "http://localhost:8080"
$env:BIG_EVENT_USERNAME = "专用测试账号"
$env:BIG_EVENT_PASSWORD = "专用测试密码"
$env:BIG_EVENT_TIMEOUT = "15"
pytest -v -s
```

将账号密码放进环境变量比长期硬编码在测试文件中更适合团队项目和 CI。

## 11. 看到失败时如何定位

1. 先看失败属于 HTTP 层还是业务层。
2. 看 `status_code`、`response.text` 和 `data["message"]`。
3. 检查测试数据是否满足后端规则，例如分类名称长度不超过 10、别名只包含字母数字。
4. 单独运行失败用例：

```powershell
pytest tests/test_category.py::test_created_category_can_be_read -v -s
```

5. 修复后运行 `pytest --lf -v -s`。

## 12. 后续学习路线

1. 使用 `responses` 或 `requests-mock` 测试网络异常，避免依赖真实后端。
2. 使用 `pytest-cov` 测 Python 业务代码覆盖率。
3. 使用 Playwright 测 Vue 页面从登录到文章管理的浏览器流程。
4. 在 GitHub Actions/Jenkins 中通过环境变量注入专用测试账号。
5. 使用工厂函数和数据类继续减少测试数据构造重复。
