import pytest

from cattle_grid.dependencies.globals import alchemy_database

from . import lifespan


@pytest.fixture(autouse=True)
async def alchemy_db():
    async with alchemy_database("sqlite+aiosqlite:///:memory:", echo=True) as engine:
        yield engine


async def test_lifespan(alchemy_db):
    async with lifespan(alchemy_db):
        pass
