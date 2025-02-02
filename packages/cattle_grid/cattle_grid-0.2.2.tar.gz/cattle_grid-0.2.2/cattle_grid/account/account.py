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


class WrongPassword(Exception):
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


async def account_with_username_password(name: str, password: str) -> Account | None:
    """Retrieves account for given username and password"""
    account = await Account.get_or_none(name=name)
    if account is None:
        return None

    try:
        password_hasher.verify(account.password_hash, password)
    except argon2.exceptions.VerifyMismatchError:
        logger.warning("Got wrong password for %s", name)
        return None

    # Implement rehash?
    # https://argon2-cffi.readthedocs.io/en/stable/howto.html

    return account


async def delete_account(name: str, password: str) -> None:
    """Deletes account for given username and password

    If password is wrong or account does not exist,
    raises a WrongPassword exception"""
    account = await account_with_username_password(name, password)
    if account is None:
        raise WrongPassword(
            "Either the account does not exist or the password is wrong"
        )

    await account.fetch_related("actors")
    if len(account.actors) > 0:
        logger.warning(
            "Deleting account with actors: %s", [a.actor for a in account.actors]
        )

    await account.delete()
