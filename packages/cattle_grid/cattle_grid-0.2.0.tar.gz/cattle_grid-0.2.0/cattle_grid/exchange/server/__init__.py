from typing import Dict
from fastapi import APIRouter
from dynaconf import LazySettings

# from .rabbit import rabbit_router
from .account import create_user_router

gateway_auth_router = APIRouter(prefix="/admin")


# gateway_auth_router.include_router(rabbit_router)


@gateway_auth_router.get("/")
async def admin_index() -> Dict[str, str]:
    return {"page": "admin_index"}


def create_exchange_api_router(config: LazySettings) -> APIRouter:
    """Creates a API Router for HTTP methods of the gateway.
    One should note that these mostly exist to fulfill secondary
    concerns of the gateway. Most of the work is done by the router.

    :param config:
    :return:
    """
    router = APIRouter()

    if config.get("gateway", {}).get("enable_authentication"):
        router.include_router(gateway_auth_router)

    router.include_router(create_user_router(config), prefix="/ap/admin")

    return router
