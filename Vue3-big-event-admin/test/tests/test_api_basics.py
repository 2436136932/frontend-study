"""服务器可达性、登录和权限基础测试。"""
from __future__ import annotations

import pytest
import requests

from conftest import (
    BASE_URL,
    BROWSER_HEADERS,
    TEST_PASSWORD,
    TEST_USERNAME,
    TIMEOUT,
    api_url,
    assert_http_ok,
    response_json,
)

pytestmark = pytest.mark.smoke


def test_api_server_is_reachable(http_session: requests.Session) -> None:
    """根地址能返回 HTTP 响应，说明服务器可达。"""
    response = http_session.get(BASE_URL, timeout=TIMEOUT)
    print(f"\n服务器状态码：{response.status_code}")
    assert response.status_code in {200, 401, 403, 404, 405}


def test_login_success(http_session: requests.Session) -> None:
    """正确账号密码应登录成功并返回 token。"""
    response = http_session.post(
        api_url("/api/login"),
        json={"username": TEST_USERNAME, "password": TEST_PASSWORD},
        timeout=TIMEOUT,
    )
    data = assert_http_ok(response)

    print(f"\n登录结果：code={data.get('code')}, message={data.get('message')}")
    assert data.get("code") == 0
    assert data.get("message") == "登录成功！"
    assert isinstance(data.get("token"), str) and data["token"]


@pytest.mark.parametrize(
    "username,password",
    [
        ("", TEST_PASSWORD),
        ("missinguser999", TEST_PASSWORD),
        (TEST_USERNAME, ""),
    ],
    ids=["empty_username", "unknown_username", "empty_password"],
)
def test_login_invalid_input_is_rejected(
    http_session: requests.Session, username: str, password: str
) -> None:
    """空字段或不存在账号应被拒绝，不应返回 token。"""
    response = http_session.post(
        api_url("/api/login"),
        json={"username": username, "password": password},
        timeout=TIMEOUT,
    )
    data = assert_http_ok(response)

    print(f"\n非法登录结果：{data}")
    assert data.get("code") != 0
    assert not data.get("token")


@pytest.mark.auth
def test_protected_endpoint_rejects_missing_token() -> None:
    """不带 token 访问用户信息应返回 401/403。"""
    response = requests.get(
        api_url("/my/userinfo"), headers=BROWSER_HEADERS, timeout=TIMEOUT
    )

    print(f"\n无 token：status={response.status_code}, body={response.text}")
    assert response.status_code in {401, 403}
    data = response_json(response)
    assert data.get("code") != 0


@pytest.mark.auth
def test_protected_endpoint_rejects_fake_token() -> None:
    """伪造 token 访问用户信息应被拒绝。"""
    headers = BROWSER_HEADERS.copy()
    headers["Authorization"] = "Bearer pytest-invalid-token"
    response = requests.get(api_url("/my/userinfo"), headers=headers, timeout=TIMEOUT)

    print(f"\n伪造 token：status={response.status_code}, body={response.text}")
    assert response.status_code in {401, 403}
    data = response_json(response)
    assert data.get("code") != 0
