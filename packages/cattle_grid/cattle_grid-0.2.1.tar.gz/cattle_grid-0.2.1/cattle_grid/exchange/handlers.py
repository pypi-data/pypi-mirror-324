import logging

from typing import Annotated
from faststream import Context
from faststream.rabbit import RabbitBroker

from cattle_grid.activity_pub.actor import (
    update_for_actor_profile,
    delete_actor,
    delete_for_actor_profile,
)
from cattle_grid.activity_pub.models import Actor
from cattle_grid.config.messaging import internal_exchange

from cattle_grid.model.exchange import (
    UpdateActorMessage,
    DeleteActorMessage,
)
from cattle_grid.model.processing import StoreActivityMessage

from .actor_update import handle_actor_action

logger = logging.getLogger(__name__)


async def update_actor(
    msg: UpdateActorMessage, broker: RabbitBroker = Context()
) -> None:
    """Should be used asynchronously"""

    actor = await Actor.get_or_none(actor_id=msg.actor)
    if actor is None:
        return

    send_update = False

    for action in msg.actions:
        if await handle_actor_action(actor, action):
            await actor.refresh_from_db()
            await actor.fetch_related("identifiers")
            send_update = True

    if msg.profile:
        actor.profile = msg.profile

        logger.info("Updating actor %s", actor.actor_id)
        await actor.save()
        await actor.fetch_related("identifiers")
        send_update = True

    if msg.autoFollow is not None:
        actor.automatically_accept_followers = msg.autoFollow
        await actor.save()

    if send_update:
        await broker.publish(
            StoreActivityMessage(actor=msg.actor, data=update_for_actor_profile(actor)),
            routing_key="store_activity",
            exchange=internal_exchange(),
        )


async def delete_actor_handler(
    msg: DeleteActorMessage, broker: Annotated[RabbitBroker, Context()]
) -> None:
    """
    Deletes the actor by id. Should be used asynchronously.

    """

    logger.info("Deleting actor %s", msg.actor)
    actor = await Actor.get_or_none(actor_id=msg.actor)

    if actor is None:
        raise ValueError("Actor not found")

    await broker.publish(
        StoreActivityMessage(
            actor=actor.actor_id, data=delete_for_actor_profile(actor)
        ),
        routing_key="store_activity",
        exchange=internal_exchange(),
    )

    await delete_actor(actor)
