from fastapi import APIRouter, HTTPException

from cattle_grid.model import FetchMessage
from cattle_grid.dependencies.fastapi import (
    Transformer,
    Broker,
    InternalExchange,
    ActivityExchange,
)

from .dependencies import CurrentAccount
from .responses import (
    LookupRequest,
)
from .requests import PerformRequest

from cattle_grid.account.models import Account, ActorForAccount


actor_router = APIRouter(prefix="/actor", tags=["actor"])


async def actor_from_account(account: Account, actor_id: str) -> ActorForAccount | None:
    await account.fetch_related("actors")

    for actor in account.actors:
        if actor.actor == actor_id:
            return actor
    return None


@actor_router.post("/lookup", response_model_exclude_none=True)
async def lookup(
    body: LookupRequest,
    account: CurrentAccount,
    broker: Broker,
    exchange: InternalExchange,
    transformer: Transformer,
) -> dict:
    actor = await actor_from_account(account, body.actor_id)
    if actor is None:
        raise HTTPException(400)

    msg = FetchMessage(actor=actor.actor, uri=body.uri)

    result = await broker.publish(
        msg, routing_key="fetch_object", exchange=exchange, rpc=True
    )

    if result is None:
        return {"raw": {}}

    return await transformer({"raw": result})


@actor_router.post("/perform", status_code=202)
async def perform_action(
    body: PerformRequest,
    account: CurrentAccount,
    broker: Broker,
    exchange: ActivityExchange,
):
    """This method allows one to trigger asynchronous activities
    through a synchronous request. The basic result is that
    the data is posted to the ActivityExchange with the
    routing_key specified.

    """

    actor = await actor_from_account(account, body.actor_id)

    if actor is None:
        raise HTTPException(400)

    await broker.publish(
        {
            "actor": body.actor_id,
            "data": body.data,
        },
        routing_key=body.action,
        exchange=exchange,
    )
