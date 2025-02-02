import logging
import re

import aiohttp
from dataclasses import dataclass
from typing import Callable, Awaitable, Dict, List
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from cattle_grid.model.lookup import LookupMethod
from cattle_grid.model.extension import MethodInformation

from cattle_grid.database import database


logger = logging.getLogger(__name__)

transformer: Callable[[Dict], Awaitable[Dict]] | None = None
lookup: LookupMethod | None = None


@dataclass
class GlobalContainer:
    session: aiohttp.ClientSession | None = None
    engine: AsyncEngine | None = None
    method_information: List[MethodInformation] | None = None

    @asynccontextmanager
    async def session_lifecycle(self):
        async with aiohttp.ClientSession() as session:
            self.session = session
            yield session

    @asynccontextmanager
    async def alchemy_database(self, db_uri, echo=False):
        if "postgres://" in db_uri:
            db_uri = db_uri.replace("postgres://", "postgresql+asyncpg://")

        self.engine = create_async_engine(db_uri, echo=echo)

        logger.info(
            "Connected to %s with sqlalchemy", re.sub("://.*@", "://***:***@", db_uri)
        )

        yield self.engine

        await self.engine.dispose()

    @asynccontextmanager
    async def common_lifecycle(self, config):
        async with database(config.db_uri, generate_schemas=False):
            async with self.session_lifecycle():
                async with self.alchemy_database(config.db_uri):
                    yield


global_container = GlobalContainer()


def get_transformer() -> Callable[[Dict], Awaitable[Dict]]:
    global transformer

    return transformer


def get_lookup() -> LookupMethod:
    global lookup

    return lookup


def get_engine() -> AsyncEngine:
    global global_container

    return global_container.engine


def get_method_information() -> List[MethodInformation]:
    global global_container

    return global_container.method_information
