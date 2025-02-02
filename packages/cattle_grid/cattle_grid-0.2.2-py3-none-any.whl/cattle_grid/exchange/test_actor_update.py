from cattle_grid.testing.fixtures import *  # noqa

from cattle_grid.activity_pub.actor import actor_to_object
from .actor_update import handle_actor_update


async def test_handle_actor_update(test_actor):
    update = {
        "action": "addIdentifier",
        "identifier": "acct:bob@localhost",
        "primary": False,
    }
    await test_actor.fetch_related("identifiers")

    assert len(test_actor.identifiers) == 1

    await handle_actor_update(test_actor, update)

    assert len(test_actor.identifiers) == 2
    assert actor_to_object(test_actor).get("preferredUsername") == "bob"


async def test_handle_actor_update_make_primary(test_actor):
    update = {
        "action": "addIdentifier",
        "identifier": "acct:bob@localhost",
        "primary": False,
    }
    await test_actor.fetch_related("identifiers")
    await handle_actor_update(test_actor, update)

    update = {
        "action": "addIdentifier",
        "identifier": "acct:alice@localhost",
        "primary": True,
    }
    await handle_actor_update(test_actor, update)

    assert len(test_actor.identifiers) == 3
    assert actor_to_object(test_actor).get("preferredUsername") == "alice"

    update = {
        "action": "makePrimary",
        "identifier": "acct:bob@localhost",
    }

    await handle_actor_update(test_actor, update)
    assert len(test_actor.identifiers) == 3
    assert actor_to_object(test_actor).get("preferredUsername") == "bob"
