from cattle_grid.testing.fixtures import database  # noqa

from .models import Account
from .account import account_with_username_password, create_account


async def test_wrong_password():
    await Account.create(
        name="name",
        password_hash="$argon2id$v=19$m=65536,t=3,p=4$MIIRqgvgQbgj220jfp0MPA$YfwJSVjtjSU0zzV/P3S9nnQ/USre2wvJMjfCIjrTQbg",
    )

    result = await account_with_username_password("name", "pass")

    assert result is None


async def test_create_and_then_get():
    username = "user"
    password = "pass"

    await create_account(username, password)

    result = await account_with_username_password(username, password)

    assert result.name == username


async def test_create_returns_none_if_user_already_exists():
    username = "user"
    password = "pass"

    await create_account(username, password)
    result = await create_account(username, password)

    assert result is None
