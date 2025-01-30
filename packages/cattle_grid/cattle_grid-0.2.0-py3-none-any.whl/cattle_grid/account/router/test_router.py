import pytest

from unittest.mock import AsyncMock

from faststream.rabbit import RabbitBroker, TestRabbitBroker, RabbitQueue

from cattle_grid.activity_pub.actor import create_actor
from cattle_grid.testing.fixtures import database  # noqa
from cattle_grid.config.messaging import internal_exchange, exchange

from .router import router, device_exchange
from cattle_grid.account.models import Account, ActorForAccount
from cattle_grid.model.extension import MethodInformation
from cattle_grid.dependencies.globals import set_method_information


@pytest.fixture
async def subscriber_mock():
    return AsyncMock()


@pytest.fixture
async def receive_subscriber_mock():
    return AsyncMock()


@pytest.fixture
async def test_account():
    return await Account.create(name="alice", password_hash="password")


@pytest.fixture
async def test_actor(test_account):
    actor = await create_actor("http://localhost/", preferred_username="alice")
    await ActorForAccount.create(actor=actor.actor_id, account=test_account)
    return actor


@pytest.fixture
async def test_broker(subscriber_mock, receive_subscriber_mock):
    br = RabbitBroker("amqp://guest:guest@localhost:5672/")
    br.include_router(router)

    async def mock(msg):
        await subscriber_mock(msg)

        return {"type": "Person", "data": "blank"}

    br.subscriber("send_message", exchange=exchange())(mock)
    br.subscriber("fetch_object", exchange=internal_exchange())(mock)

    @br.subscriber(
        RabbitQueue("queue2", routing_key="receive.*.response.*"),
        exchange=device_exchange,
    )
    async def receive_mock(msg):
        await receive_subscriber_mock(msg)

    async with TestRabbitBroker(br) as tbr:
        yield tbr


async def test_fetch_nothing_happens(test_broker, subscriber_mock):
    await test_broker.publish(
        {"uri": "http://remote/ap/actor/bob"},
        routing_key="send.alice.request.fetch",
        exchange=device_exchange,
    )

    subscriber_mock.assert_not_called()


async def test_fetch_requires_actor(test_broker, subscriber_mock):
    account = await Account.create(name="alice", password_hash="password")
    actor = await create_actor("http://localhost/", preferred_username="alice")
    await ActorForAccount.create(actor=actor.actor_id, account=account)

    fetch_uri = "http://remote/ap/actor/bob"

    await test_broker.publish(
        {
            "uri": fetch_uri,
            "actor": "http://localhost/other",
        },
        routing_key="send.alice.request.fetch",
        exchange=device_exchange,
    )

    subscriber_mock.assert_not_called()


async def test_fetch(test_broker, subscriber_mock, test_actor):
    fetch_uri = "http://remote/ap/actor/bob"

    await test_broker.publish(
        {"uri": fetch_uri, "actor": test_actor.actor_id},
        routing_key="send.alice.request.fetch",
        exchange=device_exchange,
    )

    subscriber_mock.assert_called_once()
    args = subscriber_mock.call_args[0][0]

    assert args["uri"] == fetch_uri
    assert args["actor"] == test_actor.actor_id


async def test_getting_info(test_broker, receive_subscriber_mock, test_actor):
    set_method_information([MethodInformation(routing_key="test", module="test")])

    await test_broker.publish(
        {"action": "info", "data": {}, "actor": ""},
        routing_key="send.alice.request.info",
        exchange=device_exchange,
    )

    receive_subscriber_mock.assert_called_once()
    args = receive_subscriber_mock.call_args[0][0]

    assert args["actors"] == [test_actor.actor_id]

    assert len(args["methodInformation"]) > 0
