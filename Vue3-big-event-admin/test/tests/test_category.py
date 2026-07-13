"""文章分类列表、创建、详情、编辑和自动清理测试。"""
from __future__ import annotations

import pytest
import requests

from conftest import TIMEOUT, api_url, assert_http_ok, find_category

pytestmark = [pytest.mark.auth, pytest.mark.category]


def test_category_list_schema(logged_in_session: requests.Session) -> None:
    """分类列表应为数组，每项包含 id、名称和别名。"""
    response = logged_in_session.get(api_url("/my/cate/list"), timeout=TIMEOUT)
    data = assert_http_ok(response)

    categories = data.get("data")
    print(f"\n分类数量：{len(categories)}")
    assert data.get("code") == 0
    assert isinstance(categories, list)

    for category in categories:
        assert {"id", "cate_name", "cate_alias"}.issubset(category)
        assert isinstance(category["id"], int) and category["id"] > 0
        assert isinstance(category["cate_name"], str)
        assert isinstance(category["cate_alias"], str)


@pytest.mark.write
def test_created_category_can_be_read(
    logged_in_session: requests.Session, created_category: dict
) -> None:
    """yield fixture 创建的分类应能按 ID 查询，结束后自动删除。"""
    response = logged_in_session.get(
        api_url("/my/cate/info"),
        params={"id": created_category["id"]},
        timeout=TIMEOUT,
    )
    data = assert_http_ok(response)

    print(f"\n分类详情：{data}")
    assert data.get("code") == 0
    detail = data.get("data")
    assert detail["id"] == created_category["id"]
    assert detail["cate_name"] == created_category["cate_name"]
    assert detail["cate_alias"] == created_category["cate_alias"]


@pytest.mark.write
def test_category_can_be_edited(
    logged_in_session: requests.Session, created_category: dict
) -> None:
    """只编辑 fixture 创建的分类，并验证新值。"""
    new_name = f"改{created_category['cate_alias'][-6:]}"
    new_alias = f"ed{created_category['cate_alias'][-6:]}"

    response = logged_in_session.put(
        api_url("/my/cate/info"),
        json={
            "id": created_category["id"],
            "cate_name": new_name,
            "cate_alias": new_alias,
        },
        timeout=TIMEOUT,
    )
    data = assert_http_ok(response)
    print(f"\n编辑分类结果：{data}")
    assert data.get("code") == 0

    detail_response = logged_in_session.get(
        api_url("/my/cate/info"),
        params={"id": created_category["id"]},
        timeout=TIMEOUT,
    )
    detail = assert_http_ok(detail_response).get("data")
    assert detail["cate_name"] == new_name
    assert detail["cate_alias"] == new_alias

    # fixture 清理时按 ID 删除，不依赖修改前的名称。
    created_category["cate_name"] = new_name
    created_category["cate_alias"] = new_alias


@pytest.mark.parametrize(
    "name,alias",
    [
        ("", "valid01"),
        ("合法名", ""),
        ("名称超过十个字符的测试分类", "valid02"),
        ("合法名", "bad_alias"),
    ],
    ids=["empty_name", "empty_alias", "long_name", "invalid_alias"],
)
def test_add_category_rejects_invalid_payload(
    logged_in_session: requests.Session, name: str, alias: str
) -> None:
    """非法分类数据应被后端校验拒绝。"""
    response = logged_in_session.post(
        api_url("/my/cate/add"),
        json={"cate_name": name, "cate_alias": alias},
        timeout=TIMEOUT,
    )
    data = assert_http_ok(response)

    print(f"\n非法分类 name={name!r}, alias={alias!r}：{data}")
    assert data.get("code") != 0


def test_nonexistent_category_returns_error(
    logged_in_session: requests.Session,
) -> None:
    """查询不存在的分类 ID 应返回业务错误。"""
    response = logged_in_session.get(
        api_url("/my/cate/info"), params={"id": 999999999}, timeout=TIMEOUT
    )
    data = assert_http_ok(response)
    assert data.get("code") != 0
