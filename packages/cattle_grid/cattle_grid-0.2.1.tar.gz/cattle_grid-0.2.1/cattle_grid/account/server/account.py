import logging
import aio_pika

from uuid import uuid4
from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from bovine.types import ServerSentEvent

from cattle_grid.dependencies.fastapi import Broker
from cattle_grid.activity_pub.actor import (
    create_actor,
    actor_to_object,
)
from cattle_grid.account.models import ActorForAccount

from .requests import CreateActorRequest

from .dependencies import CurrentAccount

logger = logging.getLogger(__name__)

account_router = APIRouter(prefix="/account", tags=["account"])


async def queue_for_connection(connection, username):
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    exchange = await channel.declare_exchange(
        "amq.topic", aio_pika.ExchangeType.TOPIC, durable=True
    )

    queue = await channel.declare_queue(
        f"queue-{username}-{uuid4()}",
        durable=False,
    )
    await queue.bind(exchange, routing_key=f"receive.{username}")

    return queue


def get_message_streamer(broker: Broker):
    connection = broker._connection

    async def stream_messages(username):
        try:
            async with connection:
                queue = await queue_for_connection(connection, username)

                async with queue.iterator() as iterator:
                    try:
                        async for message in iterator:
                            async with message.process():
                                message_body = message.body.decode()
                                yield message_body
                    except Exception as e:
                        logger.exception(e)
        except Exception as e:
            logger.exception(e)

    return stream_messages


@account_router.get("/stream", response_description="EventSource")
async def stream(
    account: CurrentAccount, stream_messages=Depends(get_message_streamer)
):
    """EventSource corresponding to all messages received
    by the account"""
    username = account.name

    async def event_stream():
        try:
            async for message in stream_messages(username):
                data = ServerSentEvent(data=message).encode()

                yield data
        except Exception as e:
            logger.exception(e)

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@account_router.get("/actors")
async def retrieve_actors(account: CurrentAccount) -> List[str]:
    """Returns the list of actors associated with the
    current account"""
    await account.fetch_related("actors")

    return [actor.actor for actor in account.actors]


@account_router.post("/create", status_code=201)
async def create_actor_method(body: CreateActorRequest, account: CurrentAccount):
    actor = await create_actor(body.base_url, preferred_username=body.handle)
    await actor.fetch_related("identifiers")
    await ActorForAccount.create(account=account, actor=actor.actor_id)

    return actor_to_object(actor)


@account_router.post("/delete")
async def delete_account():
    """FIXME: Implement this

    Allows one to delete the current account"""
