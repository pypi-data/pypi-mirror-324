import pytest
import json
from unittest.mock import AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient

from bovine.crypto.helper import content_digest_sha256_rfc_9530

from .router_inbox import ap_router_inbox

from cattle_grid.testing.fixtures import database, test_actor as my_actor  # noqa
from cattle_grid.config.messaging import broker


@pytest.fixture
def test_app():
    app = FastAPI()
    app.include_router(ap_router_inbox)
    return app


@pytest.fixture
def test_client(test_app):
    yield TestClient(test_app)


@pytest.fixture
def mock_broker(test_app):
    mock = AsyncMock()

    test_app.dependency_overrides[broker] = lambda: mock

    return mock


@pytest.mark.parametrize(
    ("data", "headers"),
    [
        ({}, {}),
        ({}, {"x-cattle-grid-requester": "owner"}),
        ({"actor": "other"}, {"x-cattle-grid-requester": "owner"}),
    ],
)
async def test_inbox_unauthorized(data, headers, test_client, my_actor):  # noqa
    body = json.dumps(data)
    key, val = content_digest_sha256_rfc_9530(body.encode())
    response = test_client.post(
        my_actor.inbox_uri,
        content=body,
        headers={
            key: val,
            "x-cattle-grid-requester": "owner",
            "x-ap-location": my_actor.inbox_uri,
        },
    )

    print(response.json())
    assert response.status_code == 401


async def test_inbox(test_client, my_actor, mock_broker):  # noqa
    body = b'{"actor": "owner", "type": "AnimalSound"}'
    key, val = content_digest_sha256_rfc_9530(body)

    response = test_client.post(
        my_actor.inbox_uri,
        content=body,
        headers={
            key: val,
            "x-cattle-grid-requester": "owner",
            "x-ap-location": my_actor.inbox_uri,
        },
    )

    assert response.status_code == 202

    mock_broker.publish.assert_awaited_once()


async def test_inbox_no_digest(test_client, my_actor, mock_broker):  # noqa
    response = test_client.post(
        my_actor.inbox_uri,
        json={"actor": "owner"},
        headers={
            "x-cattle-grid-requester": "owner",
            "x-ap-location": my_actor.inbox_uri,
        },
    )

    assert response.status_code == 400


async def test_inbox_unprocessable(test_client, my_actor):  # noqa
    body = b'{"xxxx"}'
    key, val = content_digest_sha256_rfc_9530(body)

    response = test_client.post(
        my_actor.inbox_uri,
        headers={
            key: val,
            "content-type": "text/plain",
            "x-cattle-grid-requester": "owner",
            "x-ap-location": my_actor.inbox_uri,
        },
        content=body,
    )

    assert response.status_code == 422


async def test_endpoint_not_found_inbox(test_client):
    response = test_client.post(
        "http://localhost/ap/inbox/not_an_actor",
        headers={
            "x-cattle-grid-requester": "owner",
            "x-ap-location": "http://localhost/ap/inbox/not_an_actor",
        },
    )

    assert response.status_code == 404
