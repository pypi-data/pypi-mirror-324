from cattle_grid.testing.fixtures import database  # noqa

from .testing import *  # noqa

from .account import get_message_streamer


def test_stream(test_app, test_client, bearer_header):
    async def streamer(username):
        yield "hello"
        yield username

    test_app.dependency_overrides[get_message_streamer] = lambda: streamer

    response = test_client.get("/account/stream", headers=bearer_header)
    assert response.status_code == 200

    assert response.headers["content-type"].split(";")[0] == "text/event-stream"

    assert (
        response.text
        == """data: hello

data: name

"""
    )


def test_actors(test_client, bearer_header):  # noqa
    response = test_client.get("/account/actors", headers=bearer_header)

    assert response.status_code == 200
    assert response.json() == []


def test_create_actor(test_client, bearer_header):
    result = test_client.post(
        "/account/create",
        json={"baseUrl": "http://abel.test"},
        headers=bearer_header,
    )
    assert result.status_code == 201

    response = test_client.get("/account/actors", headers=bearer_header)

    assert len(response.json()) == 1


def test_create_actor_with_handle(test_client, bearer_header):
    result = test_client.post(
        "/account/create",
        json={"baseUrl": "http://abel.test", "handle": "alice"},
        headers=bearer_header,
    )
    assert result.status_code == 201

    actor = result.json()
    assert actor["preferredUsername"] == "alice"
