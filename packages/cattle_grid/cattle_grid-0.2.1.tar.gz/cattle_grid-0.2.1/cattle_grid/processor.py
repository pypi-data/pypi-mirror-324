from faststream import FastStream, ContextRepo
from faststream.rabbit import RabbitBroker

import aiohttp
import logging

from contextlib import asynccontextmanager
from .account.router import create_gateway_router
from .activity_pub.processing import create_processing_router
from .exchange import create_router

from .config import load_settings
from .config.messaging import exchange, internal_exchange
from .database import database
from .testing.reporter import router as reporting_router

from .dependencies.globals import alchemy_database, set_method_information
from .exchange.info import exchange_method_information

from .extensions.load import (
    load_extensions,
    set_globals,
    lifespan_from_extensions,
    add_routers_to_broker,
    collect_method_information,
)

logging.basicConfig(level=logging.DEBUG)

settings = load_settings()

extensions = load_extensions(settings)
set_globals(extensions)


broker = RabbitBroker(settings.amqp_uri)
broker.include_router(create_gateway_router())
broker.include_router(create_processing_router(internal_exchange()))

if settings.enable_reporting:
    broker.include_router(reporting_router)

broker.include_router(create_router())

add_routers_to_broker(broker, extensions)

set_method_information(
    collect_method_information(extensions) + exchange_method_information
)


@asynccontextmanager
async def lifespan(context: ContextRepo):
    async with database(settings.db_uri, generate_schemas=False):
        async with aiohttp.ClientSession() as session:
            async with alchemy_database(settings.db_uri):
                async with lifespan_from_extensions(extensions):
                    import cattle_grid.dependencies

                    cattle_grid.dependencies.session = session
                    yield


app = FastStream(broker, lifespan=lifespan)


@app.after_startup
async def declare_exchanges() -> None:
    await broker.declare_exchange(internal_exchange())
    await broker.declare_exchange(exchange())
