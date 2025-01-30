import pytest
from cattle_grid.activity_pub.actor import create_actor
from cattle_grid.database import database as with_database

from cattle_grid.config.auth import new_auth_config, save_auth_config


@pytest.fixture(autouse=True)
async def database():
    """Fixture so that the database is initialized"""
    async with with_database(db_uri="sqlite://:memory:", generate_schemas=True):
        yield


@pytest.fixture
async def test_actor():
    """Fixture to create an actor"""
    return await create_actor("http://localhost/ap")


@pytest.fixture
def auth_config_file(tmp_path):
    config = new_auth_config(actor_id="http://localhost/actor_id", username="actor")

    filename = tmp_path / "auth_config.toml"

    config.domain_blocks = set(["blocked.example"])

    save_auth_config(filename, config)

    return filename
