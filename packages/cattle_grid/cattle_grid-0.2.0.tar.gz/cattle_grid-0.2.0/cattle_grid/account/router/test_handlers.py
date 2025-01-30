from unittest.mock import AsyncMock

from cattle_grid.account.models import Account, ActorForAccount

from cattle_grid.testing.fixtures import *  # noqa

from cattle_grid.model.account import CreateActorRequest, TriggerMessage
from .router import create_actor_handler, handle_trigger


async def test_create_actor_handler():
    account = await Account.create(name="test", password_hash="")

    broker = AsyncMock()

    await create_actor_handler(
        CreateActorRequest(base_url="http://abel", preferred_username="username"),
        account=account,
        broker=broker,
        correlation_id="uuid",
    )

    result = await ActorForAccount.filter().all()

    assert len(result) == 1

    broker.publish.assert_awaited_once()

    (data,) = broker.publish.call_args[0]

    assert data["id"] == result[0].actor
    assert data["preferredUsername"] == "username"


async def test_handle_trigger(test_actor):
    broker = AsyncMock()

    await handle_trigger(
        TriggerMessage(
            actor=test_actor.actor_id,
        ),
        actor=test_actor,
        broker=broker,
        correlation_id="uuid",
        method="method",
    )

    broker.publish.assert_awaited_once()

    (args, kwargs) = broker.publish.call_args

    assert kwargs["routing_key"] == "method"
    assert kwargs["correlation_id"] == "uuid"
