import argon2
import logging
import re

from cattle_grid.config.settings import get_settings

from .models import Account

logger = logging.getLogger(__name__)

password_hasher = argon2.PasswordHasher()


class AccountAlreadyExists(Exception):
    pass


class InvalidAccountName(Exception):
    pass


async def create_account(
    name: str, password: str, settings=get_settings()
) -> Account | None:
    """Creates a new account for username and password"""
    if await Account.get_or_none(name=name):
        raise AccountAlreadyExists("Account already exists")

    if not re.match(settings.account.allowed_name_regex, name):
        raise InvalidAccountName("Account name does not match allowed format")

    if name in settings.account.forbidden_names:
        raise InvalidAccountName("Account name is forbidden")

    return await Account.create(name=name, password_hash=password_hasher.hash(password))


async def account_with_username_password(
    username: str, password: str
) -> Account | None:
    """Retrieves account for given username and password"""
    account = await Account.get_or_none(name=username)
    if account is None:
        return None

    try:
        password_hasher.verify(account.password_hash, password)
    except argon2.exceptions.VerifyMismatchError:
        logger.warning("Got wrong password for %s", username)
        return None

    # Implement rehash?
    # https://argon2-cffi.readthedocs.io/en/stable/howto.html

    return account
