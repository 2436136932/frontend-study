"""当前用户信息接口测试，不修改真实账号资料。"""
from __future__ import annotations

import pytest
import requests

from conftest import (
    BROWSER_HEADERS,
    TEST_USERNAME,
    TIMEOUT,
    api_url,
    assert_http_ok,
)

pytestmark = [pytest.mark.auth, pytest.mark.user]


def test_current_user_schema(logged_in_session: requests.Session) -> None:
    """用户信息应属于当前账号，并包含前端需要的字段。"""
    response = logged_in_session.get(api_url("/my/userinfo"), timeout=TIMEOUT)
    data = assert_http_ok(response)

    user = data.get("data")
    print(
        "\n用户信息："
        f"id={user.get('id')}, username={user.get('username')}, "
        f"nickname={user.get('nickname')}, email={user.get('email')}"
    )
    assert data.get("code") == 0
    assert isinstance(user, dict)
    assert {"id", "username", "nickname", "email", "user_pic"}.issubset(user)
    assert user["username"] == TEST_USERNAME
    assert isinstance(user["id"], int) and user["id"] > 0
    assert isinstance(user["nickname"], str)
    assert isinstance(user["email"], str)


@pytest.mark.parametrize(
    "path,method,payload",
    [
        ("/my/userinfo", "put", {"id": 1, "nickname": "x", "email": "x@test.com"}),
        ("/my/update/avatar", "patch", {"avatar": "data:image/png;base64,AA=="}),
        (
            "/my/updatepwd",
            "patch",
            {"old_pwd": "123456", "new_pwd": "654321", "re_pwd": "654321"},
        ),
    ],
    ids=["update_profile", "update_avatar", "update_password"],
)
def test_user_write_endpoints_require_authentication(
    path: str, method: str, payload: dict
) -> None:
    """资料、头像、密码写接口在未登录时必须拒绝请求。"""
    response = requests.request(
        method,
        api_url(path),
        json=payload,
        headers=BROWSER_HEADERS,
        timeout=TIMEOUT,
    )

    print(f"\n{method.upper()} {path}：status={response.status_code}, body={response.text[:300]}")
    assert response.status_code in {401, 403}
