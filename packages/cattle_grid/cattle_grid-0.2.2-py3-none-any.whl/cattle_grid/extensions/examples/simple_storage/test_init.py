import pytest

from cattle_grid.dependencies.globals import global_container

from . import lifespan


@pytest.fixture(autouse=True)
async def alchemy_db():
    async with global_container.alchemy_database(
        "sqlite+aiosqlite:///:memory:", echo=True
    ) as engine:
        yield engine


async def test_lifespan(alchemy_db):
    async with lifespan(alchemy_db):
        pass
