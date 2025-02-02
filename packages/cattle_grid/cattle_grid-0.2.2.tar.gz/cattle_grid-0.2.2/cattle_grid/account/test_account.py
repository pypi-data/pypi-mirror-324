import pytest

from cattle_grid.testing.fixtures import database  # noqa

from .models import Account
from .account import (
    account_with_username_password,
    create_account,
    delete_account,
    AccountAlreadyExists,
    InvalidAccountName,
    WrongPassword,
)


async def test_wrong_password():
    await Account.create(
        name="name",
        password_hash="$argon2id$v=19$m=65536,t=3,p=4$MIIRqgvgQbgj220jfp0MPA$YfwJSVjtjSU0zzV/P3S9nnQ/USre2wvJMjfCIjrTQbg",
    )

    result = await account_with_username_password("name", "pass")

    assert result is None


async def test_create_and_then_get():
    name = "user"
    password = "pass"

    await create_account(name, password)

    result = await account_with_username_password(name, password)

    assert result.name == name


async def test_create_duplicate_raises_exception():
    name = "user"
    password = "pass"

    await create_account(name, password)

    with pytest.raises(AccountAlreadyExists):
        await create_account(name, password)


@pytest.mark.parametrize(
    "name", ["", "abcdefghijklmnopqrstuvwxyz", "first.second", "admin"]
)
async def test_create_name_raises_exception(name):
    with pytest.raises(InvalidAccountName):
        await create_account(name, "pass")


async def test_create_and_then_delete_wrong_password():
    name = "user"
    password = "pass"

    await create_account(name, password)

    assert 1 == await Account().filter().count()

    with pytest.raises(WrongPassword):
        await delete_account(name, "wrong")


async def test_create_and_then_delete():
    name = "user"
    password = "pass"

    await create_account(name, password)

    assert 1 == await Account().filter().count()

    await delete_account(name, password)

    assert 0 == await Account().filter().count()
