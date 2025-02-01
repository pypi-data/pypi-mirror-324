import logging
from typing import List

from fastapi import FastAPI
from faststream.rabbit import RabbitBroker
from contextlib import asynccontextmanager

from .activity_pub.server import router as ap_router
from .auth.router import create_auth_router

from .config import load_settings, default_filenames
from .config.messaging import broker
from .config.auth import get_auth_config
from .exchange.server import create_exchange_api_router
from .account.server import router as fe_router
from .account.rabbit import rabbit_router
from .extensions.load import load_extensions, add_routes_to_api, set_globals
from .dependencies.globals import alchemy_database

from .version import __version__
from .database import database, upgrade

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


tags_description = [
    {
        "name": "activity_pub",
        "description": "Endpoints used and consumed by other Fediverse applications to communicate through cattle_grid",
    },
    {
        "name": "auth",
        "description": """Authentication endpoints
    
The auth endpoint allows one to check the HTTP Signature
and reject requests with an invalid one, only based on the
headers. This step then occurs before the request is passed
to the application. Furthermore, this behavior can be shared
accross many services.""",
    },
]


def create_app(filenames: List[str] = default_filenames) -> FastAPI:
    logger.info("Running cattle grid version %s", __version__)

    base_config = load_settings(filenames=filenames)

    extensions = load_extensions(base_config)
    set_globals(extensions)

    @asynccontextmanager
    async def lifespan(app: FastAPI, broker: RabbitBroker = broker()):
        await upgrade(base_config)

        await broker.start()
        async with database(base_config.db_uri, generate_schemas=False):
            async with alchemy_database(base_config.db_uri):
                yield
        await broker.close()

    app = FastAPI(
        lifespan=lifespan,
        title="cattle_grid",
        description="middle ware for the Fediverse",
        version=__version__,
        openapi_tags=tags_description,
    )

    app.include_router(ap_router)
    app.include_router(create_exchange_api_router(base_config))
    app.include_router(create_auth_router(get_auth_config(base_config)), prefix="/auth")

    app.include_router(fe_router, prefix="/fe")
    app.include_router(rabbit_router)

    add_routes_to_api(app, extensions)

    @app.get("/")
    async def main() -> str:
        return "cattle_grid"

    return app
