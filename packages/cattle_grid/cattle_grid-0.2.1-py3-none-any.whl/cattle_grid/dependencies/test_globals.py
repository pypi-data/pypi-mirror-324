from .globals import alchemy_database, get_engine


async def test_alchemy_database():
    async with alchemy_database("sqlite+aiosqlite:///:memory:"):
        engine = get_engine()

        assert engine
