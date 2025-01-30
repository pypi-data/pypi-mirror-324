import argon2
import logging


from .models import Account

logger = logging.getLogger(__name__)

password_hasher = argon2.PasswordHasher()


async def create_account(username: str, password: str) -> Account | None:
    """Creates a new account for username and password"""
    if await Account.get_or_none(name=username):
        return None

    return await Account.create(
        name=username, password_hash=password_hasher.hash(password)
    )


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
