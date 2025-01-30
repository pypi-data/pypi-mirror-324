from fastapi import APIRouter, Form, Header, HTTPException
from dynaconf import LazySettings

from urllib.parse import urljoin
from typing import Annotated, Dict, Any

from cattle_grid.config import load_settings
from cattle_grid.activity_pub.actor import create_actor, actor_to_object
from cattle_grid.activity_pub.models import Actor
from cattle_grid.account.models import ActorForAccount, Account
from cattle_grid.account.account import create_account


def create_user_router(base_config: LazySettings = load_settings()) -> APIRouter:
    user_router = APIRouter(tags=["user"])

    config = base_config.gateway.admin

    if not config.enable:
        return user_router

    @user_router.post("/create", status_code=201)
    async def post_create_user(
        username: Annotated[str, Form()],
        password: Annotated[str, Form()],
        x_ap_location: Annotated[str, Header()],
    ) -> Dict[str, Any]:
        account = await create_account(username, password)

        if not account:
            raise HTTPException(409)

        url_base = urljoin(x_ap_location, "/")

        actor = await create_actor(url_base, preferred_username=username)
        await ActorForAccount.create(account=account, actor=actor.actor_id)

        return actor_to_object(actor)

    if not config.enable_reset:
        return user_router

    @user_router.post("/delete")
    async def delete_user(username: Annotated[str, Form()]) -> Dict[str, str]:
        user = await Account.get(name=username).prefetch_related("actors")

        for actor in user.actors:
            to_delete = await Actor.get(actor_id=actor.actor)
            await to_delete.delete()

        await user.delete()
        return {"status": "done"}

    return user_router
