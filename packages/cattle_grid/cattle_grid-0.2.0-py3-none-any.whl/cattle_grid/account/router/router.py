import asyncio
import logging
from faststream import Context
from faststream.rabbit import RabbitRouter, RabbitBroker, RabbitQueue

from cattle_grid.activity_pub.actor import (
    create_actor,
    actor_to_object,
)

from cattle_grid.config.settings import get_settings
from cattle_grid.config.messaging import internal_exchange, exchange

from cattle_grid.model.account import (
    FetchMessage,
    FetchResponse,
    TriggerMessage,
    InformationResponse,
    CreateActorRequest,
)

from cattle_grid.account.models import ActorForAccount
from cattle_grid.dependencies import CorrelationId, MethodInformation

from .info import protocol_and_backend
from .exchange import device_exchange
from .annotations import (
    AccountName,
    AccountFromRoutingKey,
    ActorFromMessage,
    MethodFromRoutingKey,
)
from .exception import exception_middleware

logger = logging.getLogger(__name__)

router = RabbitRouter(middlewares=[exception_middleware])


info_publisher = router.publisher(
    "receive.name.response.fetch",
    schema=FetchResponse,
    title="receive.NAME.response.fetch",
)


@router.subscriber(
    RabbitQueue(
        "send_request_fetch",
        routing_key="send.*.request.fetch",
    ),
    exchange=device_exchange,
    title="send.*.request.fetch",
)
async def handle_fetch(
    msg: FetchMessage,
    correlation_id: CorrelationId,
    name: AccountName,
    actor: ActorFromMessage,
    broker: RabbitBroker = Context(),
):
    """Used to retrieve an object"""
    try:
        async with asyncio.timeout(0.5):
            result = await broker.publish(
                {"actor": actor.actor_id, "uri": msg.uri},
                routing_key="fetch_object",
                exchange=internal_exchange(),
                rpc=True,
            )
        if result == b"":
            result = None
        logger.info("GOT result %s", result)
    except TimeoutError as e:
        logger.error("Request ran into timeout %s", e)
        result = None

    if result:
        await broker.publish(
            FetchResponse(
                uri=msg.uri,
                actor=actor.actor_id,
                data=result,
            ),
            routing_key=f"receive.{name}.response.fetch",
            exchange=device_exchange,
            correlation_id=correlation_id,
        )
    else:
        await broker.publish(
            {
                "message": "Could not fetch object",
            },
            routing_key=f"error.{name}",
            exchange=device_exchange,
            correlation_id=correlation_id,
        )


info_publisher = router.publisher(
    "receive.name.response.info",
    schema=InformationResponse,
    title="receive.NAME.response.info",
)


@router.subscriber(
    RabbitQueue(
        "send_request_info",
        routing_key="send.*.request.info",
    ),
    exchange=device_exchange,
    title="send.*.request.info",
)
async def information_request_handler(
    account: AccountFromRoutingKey,
    correlation_id: CorrelationId,
    method_information: MethodInformation,
    broker: RabbitBroker = Context(),
) -> None:
    """Provides information about the underlying service"""
    actor_ids = [x.actor for x in account.actors]

    await info_publisher.publish(
        InformationResponse(
            base_urls=get_settings().frontend.base_urls,
            actors=actor_ids,
            **protocol_and_backend(),
            method_information=method_information,
        ),
        routing_key=f"receive.{account.name}.response.info",
        exchange=device_exchange,
        correlation_id=correlation_id,
    )


info_publisher = router.publisher(
    "receive.name.response.create_actor",
    schema=dict,
    title="receive.NAME.response.create_actor",
    description="""The response to a create_actor request
is the actor profile (as formatted towards the Fediverse)
This might change in the future""",
)


@router.subscriber(
    RabbitQueue(
        "send_request_create_actor",
        routing_key="send.*.request.create_actor",
    ),
    exchange=device_exchange,
    title="send.*.request.create_actor",
)
async def create_actor_handler(
    create_message: CreateActorRequest,
    correlation_id: CorrelationId,
    account: AccountFromRoutingKey,
    broker: RabbitBroker = Context(),
) -> None:
    """Creates an actor associated with the account.

    Updating and deleting actors is done through trigger events."""

    allowed_base_urls = get_settings().frontend.base_urls
    if create_message.base_url not in allowed_base_urls:
        raise ValueError(f"Base URL {create_message.base_url} not in allowed base urls")

    actor = await create_actor(
        create_message.base_url,
        preferred_username=create_message.preferred_username,
        profile=create_message.profile,
    )

    await ActorForAccount.create(account=account, actor=actor.actor_id)

    if create_message.automatically_accept_followers:
        actor.automatically_accept_followers = True
        await actor.save()

    result = actor_to_object(actor)

    logger.info("Created actor %s for %s", actor.actor_id, account.name)

    await broker.publish(
        result,
        routing_key=f"receive.{account.name}.response.create_actor",
        exchange=device_exchange,
        correlation_id=correlation_id,
    )


@router.subscriber(
    RabbitQueue(
        "send_trigger",
        routing_key="send.*.trigger.#",
    ),
    exchange=device_exchange,
    title="send.*.trigger.#",
)
async def handle_trigger(
    msg: TriggerMessage,
    actor: ActorFromMessage,
    correlation_id: CorrelationId,
    method: MethodFromRoutingKey,
    broker: RabbitBroker = Context(),
):
    """Used to trigger a method performed by the actor.

    The main thing an actor can do is send activities to
    the Fediverse. This can be done with `send_message`.
    This can be extended in cattle_grid through extensions.

    However the methods to update the actor profile and delete
    the actor are also called via a trigger.
    """
    await broker.publish(
        msg,
        routing_key=method,
        exchange=exchange(),
        correlation_id=correlation_id,
    )
