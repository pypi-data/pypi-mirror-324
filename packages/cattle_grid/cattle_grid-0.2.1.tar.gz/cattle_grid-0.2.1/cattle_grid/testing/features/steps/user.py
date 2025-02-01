import logging
import asyncio
from behave import given, when
from behave.api.async_step import async_run_until_complete

from almabtrieb import Almabtrieb

from cattle_grid.model.exchange import UpdateActorMessage

from cattle_grid.testing.features import publish_as

logger = logging.getLogger(__name__)


async def create_user_on_server(context, username, hostname) -> None:
    """Helper routine that creates a user on the server.

    The user object and Listener are stored in
    `context.actors[username]` and `context.listeners[username]`
    respectively."""
    response = await context.session.post(
        f"http://{hostname}/admin/create",
        data={"username": username, "password": username},
    )

    if response.status == 409:
        logger.warning("User already exists deleting")
        response = await context.session.post(
            "http://abel/admin/delete", data={"username": username}
        )

        assert response.status == 200

        response = await context.session.post(
            f"http://{hostname}/admin/create",
            data={"username": username, "password": username},
        )

    assert response.status == 201

    context.actors[username] = await response.json()

    context.connections[username] = Almabtrieb.from_connection_string(
        f"amqp://{username}:{username}@rabbitmq/", silent=True
    )
    context.connections[username].task = asyncio.create_task(
        context.connections[username].run()
    )

    while not context.connections[username].connected:
        await asyncio.sleep(0.1)
        # logger.info("Waiting for connection")


@given('A new user called "{username}" on "{hostname}"')
@async_run_until_complete
async def new_user_on_server(context, username, hostname):
    await create_user_on_server(context, username, hostname)


@given('A new user called "{username}"')
@async_run_until_complete
async def new_user(context, username):
    """Creates a new user

    Usage example:

    ```gherkin
    Given A new user called "Alice"
    ```
    """
    hostname = {"alice": "abel", "bob": "banach", "Bob": "banach"}.get(username, "abel")

    await create_user_on_server(context, username, hostname)


@when('"{alice}" updates her profile')
@async_run_until_complete
async def update_profile(context, alice):
    """
    ```gherkin
    When "Alice" updates her profile
    ```
    """

    for connection in context.connections.values():
        await connection.clear_incoming()

    alice_id = context.actors[alice].get("id")

    msg = UpdateActorMessage(
        actor=alice_id, profile={"summary": "I love cows"}
    ).model_dump()

    await publish_as(context, alice, "update_actor", msg)


@when('"{alice}" deletes herself')
@when('"{alice}" deletes himself')
@async_run_until_complete
async def actor_deletes_themselves(context, alice):
    """
    ```gherkin
    When "Alice" deletes herself
    When "Bob" deletes himself
    ```
    """
    alice_id = context.actors[alice].get("id")

    await publish_as(
        context,
        alice,
        "delete_actor",
        {
            "actor": alice_id,
        },
    )
