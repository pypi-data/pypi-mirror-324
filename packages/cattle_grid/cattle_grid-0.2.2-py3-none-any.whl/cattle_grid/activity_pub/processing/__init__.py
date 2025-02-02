from faststream.rabbit import RabbitRouter, RabbitExchange, RabbitQueue
from typing import Callable, Any, Awaitable, List, Tuple

from cattle_grid.config.messaging import internal_exchange

from .remote import fetch_object, sending_message
from .outgoing import create_outgoing_router
from .incoming import create_incoming_router
from .store_activity import store_activity_subscriber


def create_processing_router(
    exchange: RabbitExchange = internal_exchange(),
) -> RabbitRouter:
    router = RabbitRouter()
    router.include_router(create_outgoing_router(exchange))
    router.include_router(create_incoming_router(exchange))

    routing_config: List[Tuple[str, Callable[[Any], Awaitable[Any]]]] = [
        ("store_activity", store_activity_subscriber),
        ("to_send", sending_message),
        ("fetch_object", fetch_object),
    ]
    for routing_key, coroutine in routing_config:
        router.subscriber(
            RabbitQueue(f"cg_internal_{routing_key}", routing_key=routing_key),
            exchange=exchange,
            title=f"Internal:{routing_key}",
        )(coroutine)

    return router


processing_router = create_processing_router()
