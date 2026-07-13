"""文章列表、筛选、详情和安全 CRUD 测试。"""
from __future__ import annotations

import pytest
import requests

from conftest import TIMEOUT, api_url, assert_http_ok, make_test_jpeg

pytestmark = [pytest.mark.auth, pytest.mark.article]


@pytest.mark.parametrize("page_size", [1, 2, 5], ids=lambda size: f"pagesize_{size}")
def test_article_list_pagination(
    logged_in_session: requests.Session, page_size: int
) -> None:
    """返回数量不能超过请求的每页条数。"""
    response = logged_in_session.get(
        api_url("/my/article/list"),
        params={"pagenum": 1, "pagesize": page_size},
        timeout=TIMEOUT,
    )
    data = assert_http_ok(response)

    articles = data.get("data")
    print(
        f"\npagesize={page_size}, total={data.get('total')}, "
        f"returned={len(articles)}"
    )
    assert data.get("code") == 0
    assert isinstance(data.get("total"), int)
    assert isinstance(articles, list)
    assert len(articles) <= page_size


@pytest.mark.parametrize("state", ["已发布", "草稿"], ids=["published", "draft"])
def test_article_list_filter_by_state(
    logged_in_session: requests.Session, state: str
) -> None:
    """按状态筛选后，每一条返回记录都应匹配。"""
    response = logged_in_session.get(
        api_url("/my/article/list"),
        params={"pagenum": 1, "pagesize": 20, "state": state},
        timeout=TIMEOUT,
    )
    data = assert_http_ok(response)

    articles = data.get("data")
    print(f"\nstate={state}, 返回 {len(articles)} 条")
    assert data.get("code") == 0
    assert isinstance(articles, list)
    assert all(article.get("state") == state for article in articles)


def test_article_list_item_schema(logged_in_session: requests.Session) -> None:
    """文章列表项应包含前端表格使用的字段。"""
    response = logged_in_session.get(
        api_url("/my/article/list"),
        params={"pagenum": 1, "pagesize": 5},
        timeout=TIMEOUT,
    )
    data = assert_http_ok(response)
    articles = data.get("data")

    assert isinstance(articles, list)
    for article in articles:
        assert {"id", "title", "pub_date", "state", "cate_name"}.issubset(article)


@pytest.mark.write
def test_created_article_detail(
    logged_in_session: requests.Session, created_article: dict
) -> None:
    """fixture 发布的文章应能查到完整详情。"""
    response = logged_in_session.get(
        api_url("/my/article/info"),
        params={"id": created_article["id"]},
        timeout=TIMEOUT,
    )
    data = assert_http_ok(response)

    print(f"\n文章详情：{data}")
    assert data.get("code") == 0
    detail = data.get("data")
    assert {
        "id",
        "title",
        "content",
        "cover_img",
        "state",
        "cate_id",
    }.issubset(detail)
    assert detail["id"] == created_article["id"]
    assert detail["title"] == created_article["title"]


@pytest.mark.write
def test_created_article_can_be_edited(
    logged_in_session: requests.Session, created_article: dict
) -> None:
    """只编辑 fixture 创建的文章，并验证修改结果。"""
    detail_response = logged_in_session.get(
        api_url("/my/article/info"),
        params={"id": created_article["id"]},
        timeout=TIMEOUT,
    )
    detail = assert_http_ok(detail_response).get("data")
    new_title = f"已改{created_article['id']}"

    edit_response = logged_in_session.put(
        api_url("/my/article/info"),
        data={
            "id": str(created_article["id"]),
            "title": new_title,
            "cate_id": str(detail["cate_id"]),
            "content": "<p>pytest 编辑后的内容</p>",
            "state": "已发布",
        },
        files={"cover_img": ("pytest-cover.jpg", make_test_jpeg(), "image/jpeg")},
        timeout=TIMEOUT,
    )
    edit_data = assert_http_ok(edit_response)
    print(f"\n编辑文章结果：{edit_data}")
    assert edit_data.get("code") == 0

    verify_response = logged_in_session.get(
        api_url("/my/article/info"),
        params={"id": created_article["id"]},
        timeout=TIMEOUT,
    )
    updated = assert_http_ok(verify_response).get("data")
    assert updated["title"] == new_title
    assert updated["state"] == "已发布"

    created_article["title"] = new_title


def test_nonexistent_article_returns_error(
    logged_in_session: requests.Session,
) -> None:
    """不存在的文章 ID 应返回业务错误。"""
    response = logged_in_session.get(
        api_url("/my/article/info"), params={"id": 999999999}, timeout=TIMEOUT
    )
    data = assert_http_ok(response)
    assert data.get("code") != 0


def test_publish_article_requires_title(
    logged_in_session: requests.Session, created_category: dict
) -> None:
    """缺少标题时，即使其他 multipart 字段存在也应失败。"""
    response = logged_in_session.post(
        api_url("/my/article/add"),
        data={
            "cate_id": str(created_category["id"]),
            "content": "<p>缺少标题</p>",
            "state": "草稿",
        },
        files={"cover_img": ("pytest-cover.jpg", make_test_jpeg(), "image/jpeg")},
        timeout=TIMEOUT,
    )
    data = assert_http_ok(response)
    print(f"\n缺少标题的发布结果：{data}")
    assert data.get("code") != 0
