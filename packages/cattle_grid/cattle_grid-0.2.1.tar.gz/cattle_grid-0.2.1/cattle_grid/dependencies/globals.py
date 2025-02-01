import logging
import re


from typing import Callable, Awaitable, Dict, List
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from cattle_grid.model.lookup import LookupMethod
from cattle_grid.model.extension import MethodInformation

logger = logging.getLogger(__name__)

transformer: Callable[[Dict], Awaitable[Dict]] | None = None
lookup: LookupMethod | None = None
engine: AsyncEngine | None = None
method_information: List[MethodInformation] | None = None


def get_transformer() -> Callable[[Dict], Awaitable[Dict]]:
    global transformer

    return transformer


def get_lookup() -> LookupMethod:
    global lookup

    return lookup


def get_engine() -> AsyncEngine:
    global engine

    return engine


@asynccontextmanager
async def alchemy_database(db_uri, echo=False):
    global engine

    if "postgres://" in db_uri:
        db_uri = db_uri.replace("postgres://", "postgresql+asyncpg://")

    engine = create_async_engine(db_uri, echo=echo)

    logger.info(
        "Connected to %s with sqlalchemy", re.sub("://.*@", "://***:***@", db_uri)
    )

    yield engine

    await engine.dispose()


def get_method_information() -> List[MethodInformation]:
    global method_information

    return method_information


def set_method_information(new_method_information: List[MethodInformation]):
    global method_information

    method_information = new_method_information
