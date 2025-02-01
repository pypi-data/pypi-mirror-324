from contextlib import asynccontextmanager
from typing import Annotated

from fast_depends import Depends
from fastapi import Depends as FADepends

from cattle_grid.dependencies import SqlAsyncEngine
from cattle_grid.dependencies.fastapi import SqlAsyncEngine as FastAPISqlEngine

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from .models import Base


@asynccontextmanager
async def lifespan(engine: SqlAsyncEngine):
    """The lifespan ensure that the necessary database table is
    created."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


async def with_session_commit(sql_engine: SqlAsyncEngine):
    async with async_sessionmaker(sql_engine)() as session:
        yield session
        await session.commit()


async def with_fast_api_session(sql_engine: FastAPISqlEngine):
    async with async_sessionmaker(sql_engine)() as session:
        yield session


CommittingSession = Annotated[AsyncSession, Depends(with_session_commit)]
"""Session that commits the transaction"""

FastApiSession = Annotated[AsyncSession, FADepends(with_fast_api_session)]
"""Session annotation to be used with FastAPI"""
