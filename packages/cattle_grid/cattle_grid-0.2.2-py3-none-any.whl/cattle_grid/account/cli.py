import click
import asyncio


from cattle_grid.database import database
from .models import Account
from .account import create_account


async def new_account(config, name, password):
    async with database(db_uri=config.db_uri):
        await create_account(name, password)


async def list_accounts(config):
    async with database(db_uri=config.db_uri):
        accounts = await Account.all()
        for account in accounts:
            print(account.name)


def add_account_commands(main):
    @main.group()
    def account():
        """Used to manage accounts associated with cattle_grid"""

    @account.command()
    @click.argument("name")
    @click.argument("password")
    @click.pass_context
    def new(cfg, name, password):
        """Creates a new account"""
        asyncio.run(new_account(cfg.obj["config"], name, password))

    @account.command()
    @click.pass_context
    def list(cfg):
        """Lists existing accounts"""
        asyncio.run(list_accounts(cfg.obj["config"]))
