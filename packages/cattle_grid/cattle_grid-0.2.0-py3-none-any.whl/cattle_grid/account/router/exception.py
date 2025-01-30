from faststream.rabbit import RabbitBroker
from faststream import ExceptionMiddleware, Context

import logging

from cattle_grid.model.account import ErrorMessage
from cattle_grid.dependencies import CorrelationId

from .annotations import AccountName, RoutingKey
from .exchange import device_exchange

logger = logging.getLogger(__name__)

exception_middleware = ExceptionMiddleware()


@exception_middleware.add_handler(Exception)
async def exception_handler(
    exception: Exception,
    name: AccountName,
    routing_key: RoutingKey,
    correlation_id: CorrelationId,
    broker: RabbitBroker = Context(),
):
    logger.error("Processing error occurred for %s", name)
    logger.exception(exception)

    await broker.publish(
        ErrorMessage(message=str(exception), routing_key=routing_key),
        routing_key=f"error.{name}",
        exchange=device_exchange,
        correlation_id=correlation_id,
    )
