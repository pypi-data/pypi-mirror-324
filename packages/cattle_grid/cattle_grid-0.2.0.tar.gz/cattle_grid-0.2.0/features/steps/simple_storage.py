from behave import when
from behave.api.async_step import async_run_until_complete

from bovine.activitystreams import factories_for_actor_object

from cattle_grid.testing.features import publish_as


@when('"{alice}" publishes a "{moo}" animal sound to her follows')
@async_run_until_complete
async def send_sound(context, alice, moo):
    for connection in context.connections.values():
        await connection.clear_incoming()

    alice_actor = context.actors[alice]
    activity_factory, _ = factories_for_actor_object(alice_actor)

    activity = (
        activity_factory.custom(type="AnimalSound", content="moo").as_public().build()
    )

    await publish_as(
        context,
        alice,
        "publish_activity",
        {"actor": context.actors[alice].get("id"), "data": activity},
    )
