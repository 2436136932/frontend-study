"""大事件管理系统 API 测试的公共配置、工具函数和 fixtures。"""
from __future__ import annotations

import io
import os
import uuid
from collections.abc import Generator

import pytest
import requests

BASE_URL = os.getenv(
    "BIG_EVENT_BASE_URL", "https://big-event-vue-api-t.itheima.net"
).rstrip("/")
TEST_USERNAME = os.getenv("BIG_EVENT_USERNAME", "2436136932")
TEST_PASSWORD = os.getenv("BIG_EVENT_PASSWORD", "123456")
TIMEOUT = float(os.getenv("BIG_EVENT_TIMEOUT", "10"))

BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Origin": BASE_URL,
    "Referer": BASE_URL + "/",
}


def api_url(path: str) -> str:
    """把相对接口路径拼接成完整 URL。"""
    return f"{BASE_URL}{path}"


def response_json(response: requests.Response) -> dict:
    """解析 JSON；解析失败时把原始响应放进断言信息。"""
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError as error:
        raise AssertionError(
            f"接口未返回 JSON：status={response.status_code}, body={response.text[:500]}"
        ) from error


def assert_http_ok(response: requests.Response) -> dict:
    """断言 HTTP 200，并返回解析后的 JSON。"""
    assert response.status_code == 200, (
        f"HTTP 请求失败：status={response.status_code}, body={response.text[:500]}"
    )
    return response_json(response)


def unique_suffix() -> str:
    """生成短且唯一的字母数字后缀，满足后端字段校验。"""
    return uuid.uuid4().hex[:6]


def find_category(session: requests.Session, *, name: str, alias: str) -> dict | None:
    """按名称和别名精确查找分类。"""
    response = session.get(api_url("/my/cate/list"), timeout=TIMEOUT)
    data = assert_http_ok(response)
    assert data.get("code") == 0, data

    for category in data.get("data", []):
        if category.get("cate_name") == name and category.get("cate_alias") == alias:
            return category
    return None


def category_exists_by_id(session: requests.Session, category_id: int) -> bool:
    """判断指定分类 ID 是否仍存在。"""
    response = session.get(
        api_url("/my/cate/info"), params={"id": category_id}, timeout=TIMEOUT
    )
    data = assert_http_ok(response)
    return data.get("code") == 0


def article_exists_by_id(session: requests.Session, article_id: int) -> bool:
    """判断指定文章 ID 是否仍存在。"""
    response = session.get(
        api_url("/my/article/info"), params={"id": article_id}, timeout=TIMEOUT
    )
    data = assert_http_ok(response)
    return data.get("code") == 0


def find_article(session: requests.Session, *, title: str) -> dict | None:
    """分页查找标题唯一的测试文章。"""
    page = 1
    page_size = 20

    while page <= 20:
        response = session.get(
            api_url("/my/article/list"),
            params={"pagenum": page, "pagesize": page_size},
            timeout=TIMEOUT,
        )
        data = assert_http_ok(response)
        assert data.get("code") == 0, data

        articles = data.get("data", [])
        for article in articles:
            if article.get("title") == title:
                return article

        total = data.get("total", 0)
        if page * page_size >= total or not articles:
            break
        page += 1

    return None


def make_test_jpeg() -> io.BytesIO:
    """生成测试上传使用的最小 JPEG 文件对象。"""
    jpeg = bytes.fromhex(
        "FFD8FFE000104A46494600010100000100010000"
        "FFDB004300080606070605080707070909080A0C140D0C0B0B0C1912130F141D"
        "1A1F1E1D1A1C1C20242E2720222C231C1C2837292C30313434341F27393D3832"
        "3C2E333432FFC0000B080001000101011100FFC4001400010000000000000000"
        "0000000000000003FFC40014100100000000000000000000000000000000FFDA"
        "0008010100003F0037FFD9"
    )
    image = io.BytesIO(jpeg)
    image.name = "pytest-cover.jpg"
    return image


@pytest.fixture(scope="session")
def http_session() -> Generator[requests.Session, None, None]:
    """整个测试会话复用同一个 HTTP 连接池。"""
    session = requests.Session()
    session.headers.update(BROWSER_HEADERS)
    yield session
    session.close()


@pytest.fixture(scope="session")
def logged_in_session(
    http_session: requests.Session,
) -> Generator[requests.Session, None, None]:
    """登录一次，并为后续请求自动携带 Authorization。"""
    response = http_session.post(
        api_url("/api/login"),
        json={"username": TEST_USERNAME, "password": TEST_PASSWORD},
        timeout=TIMEOUT,
    )
    data = assert_http_ok(response)
    assert data.get("code") == 0, f"测试账号登录失败：{data}"
    assert data.get("token"), f"登录响应缺少 token：{data}"

    http_session.headers["Authorization"] = data["token"]
    print(f"\nfixture：账号 {TEST_USERNAME} 登录成功")
    yield http_session
    http_session.headers.pop("Authorization", None)


@pytest.fixture
def created_category(
    logged_in_session: requests.Session,
) -> Generator[dict, None, None]:
    """创建测试分类，yield 给测试，测试结束后自动删除。"""
    suffix = unique_suffix()
    name = f"测{suffix}"
    alias = f"pt{suffix}"

    create_response = logged_in_session.post(
        api_url("/my/cate/add"),
        json={"cate_name": name, "cate_alias": alias},
        timeout=TIMEOUT,
    )
    create_data = assert_http_ok(create_response)
    assert create_data.get("code") == 0, f"测试分类创建失败：{create_data}"

    category = find_category(logged_in_session, name=name, alias=alias)
    assert category is not None, "创建接口返回成功，但分类列表中找不到测试分类"
    print(f"\nfixture：已创建测试分类 {category}")

    try:
        yield category
    finally:
        delete_response = logged_in_session.delete(
            api_url("/my/cate/del"),
            params={"id": category["id"]},
            timeout=TIMEOUT,
        )
        delete_data = assert_http_ok(delete_response)
        if delete_data.get("code") == 0:
            print(f"fixture：已清理测试分类 id={category['id']}")
        else:
            # 测试本身可能已经删除了该分类；按唯一 ID 核验是否仍存在。
            assert not category_exists_by_id(
                logged_in_session, category["id"]
            ), f"测试分类自动清理失败：{delete_data}"


@pytest.fixture
def created_article(
    logged_in_session: requests.Session,
    created_category: dict,
) -> Generator[dict, None, None]:
    """创建测试文章，yield 给测试，测试结束后自动删除。"""
    title = f"pytest文章{unique_suffix()}"
    publish_response = logged_in_session.post(
        api_url("/my/article/add"),
        data={
            "title": title,
            "cate_id": str(created_category["id"]),
            "content": "<p>pytest 自动化测试内容</p>",
            "state": "草稿",
        },
        files={"cover_img": ("pytest-cover.jpg", make_test_jpeg(), "image/jpeg")},
        timeout=TIMEOUT,
    )
    publish_data = assert_http_ok(publish_response)
    assert publish_data.get("code") == 0, f"测试文章创建失败：{publish_data}"

    article = find_article(logged_in_session, title=title)
    assert article is not None, "发布接口返回成功，但文章列表中找不到测试文章"
    print(f"\nfixture：已创建测试文章 {article}")

    try:
        yield article
    finally:
        delete_response = logged_in_session.delete(
            api_url("/my/article/info"),
            params={"id": article["id"]},
            timeout=TIMEOUT,
        )
        delete_data = assert_http_ok(delete_response)
        if delete_data.get("code") == 0:
            print(f"fixture：已清理测试文章 id={article['id']}")
        else:
            assert not article_exists_by_id(
                logged_in_session, article["id"]
            ), f"测试文章自动清理失败：{delete_data}"
