from faststream import FastStream
from faststream.rabbit import RabbitBroker

import logging

from contextlib import asynccontextmanager

from .app import add_routers_to_broker, init_extensions

from .config import load_settings
from .config.messaging import exchange, internal_exchange

from .dependencies.globals import global_container

from .extensions.load import (
    lifespan_from_extensions,
)

logging.basicConfig(level=logging.DEBUG)

settings = load_settings()
extensions = init_extensions(settings)

broker = RabbitBroker(settings.amqp_uri)

add_routers_to_broker(broker, extensions, settings)


@asynccontextmanager
async def lifespan():
    async with global_container.common_lifecycle(settings):
        async with lifespan_from_extensions(extensions):
            yield


app = FastStream(broker, lifespan=lifespan)


@app.after_startup
async def declare_exchanges() -> None:
    await broker.declare_exchange(internal_exchange())
    await broker.declare_exchange(exchange())
