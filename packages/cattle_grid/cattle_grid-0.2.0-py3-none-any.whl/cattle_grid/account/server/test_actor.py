import pytest

from unittest.mock import AsyncMock

from cattle_grid.testing.fixtures import database  # noqa
from cattle_grid.dependencies.globals import get_transformer

from .testing import *  # noqa


@pytest.mark.parametrize(
    "endpoint,data",
    [
        ("/actor/lookup", {"actorId": "bad_actor", "uri": "http://remote.test/"}),
        ("/actor/perform", {"actorId": "bad_actor", "data": {}, "action": "none"}),
    ],
)
def test_lookup_bad_actor(test_client, bearer_header, endpoint, data):
    result = test_client.post(
        endpoint,
        json=data,
        headers=bearer_header,
    )

    assert result.status_code == 400


def test_lookup_no_result(test_app, test_client, bearer_header, test_broker):
    result = test_client.post(
        "/account/create",
        json={"baseUrl": "http://abel.test"},
        headers=bearer_header,
    )
    assert result.status_code == 201
    actor_id = result.json()["id"]

    test_broker.publish = AsyncMock(return_value=None)
    result = test_client.post(
        "/actor/lookup",
        json={"actorId": actor_id, "uri": "http://remote.test/"},
        headers=bearer_header,
    )

    assert result.status_code == 200
    assert result.json() == {"raw": {}}


def test_lookup_result(test_app, test_client, bearer_header, test_broker):
    result = test_client.post(
        "/account/create",
        json={"baseUrl": "http://abel.test"},
        headers=bearer_header,
    )
    assert result.status_code == 201
    actor_id = result.json()["id"]

    test_app.dependency_overrides[get_transformer] = lambda: AsyncMock(
        side_effect=lambda x: x
    )

    test_broker.publish = AsyncMock(return_value={"data": 1})

    result = test_client.post(
        "/actor/lookup",
        json={"actorId": actor_id, "uri": "http://remote.test/"},
        headers=bearer_header,
    )

    assert result.status_code == 200
    assert result.json() == {"raw": {"data": 1}}


def test_perform_action(test_app, test_client, bearer_header, test_broker):
    result = test_client.post(
        "/account/create",
        json={"baseUrl": "http://abel.test"},
        headers=bearer_header,
    )
    assert result.status_code == 201
    actor_id = result.json()["id"]

    result = test_client.post(
        "/actor/perform",
        json={"actorId": actor_id, "action": "send", "data": {"moo": True}},
        headers=bearer_header,
    )

    assert result.status_code == 202
    test_broker.publish.assert_awaited_once()
