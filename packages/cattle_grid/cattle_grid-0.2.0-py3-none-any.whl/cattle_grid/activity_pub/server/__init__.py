"""This package contains the overall router for all connection
needs to the Fediverse. This means the .well-known endpoints."""

import logging

from fastapi import APIRouter, HTTPException, Header

from typing import Annotated

from bovine.utils import webfinger_response
from bovine.models import JrdData, JrdLink

from .router import ap_router
from .router_inbox import ap_router_inbox
from .router_object import ap_router_object
from cattle_grid.activity_pub.models import PublicIdentifier

logger = logging.getLogger(__name__)

router = APIRouter(tags=["activity_pub"], prefix="/ap")
router.include_router(ap_router)
router.include_router(ap_router_inbox)
router.include_router(ap_router_object)


@router.get("/")
async def main() -> str:
    return "cattle_grid ap endpoint"


@router.get("/.well-known/webfinger")
async def webfinger_responder(resource: str) -> JrdData:
    """Handles requests to .well-known/webfinger. Results are determined by the identifier property of [PublicIdentifier][cattle_grid.activity_pub.models.PublicIdentifier] matching the resource
    parameter.

    See [RFC 7033 WebFinger](https://www.rfc-editor.org/rfc/rfc7033).
    """

    logger.info("looking up web finger for resource '%s'", resource)

    pi = await PublicIdentifier.get_or_none(identifier=resource)
    if not pi:
        raise HTTPException(status_code=404, detail="Item not found")

    await pi.fetch_related("actor")

    return webfinger_response(pi.identifier, pi.actor.actor_id)


@router.get("/.well-known/nodeinfo", response_model_exclude_none=True)
async def nodeinfo_responder(x_ap_location: Annotated[str, Header()]) -> JrdData:
    return JrdData(
        links=[
            JrdLink(
                type="http://nodeinfo.diaspora.software/ns/schema/2.0",
                href=x_ap_location + "_2.0",
            )
        ]
    )


@router.get("/.well-known/nodeinfo_2.0")
async def nodeinfo_data_responder() -> dict:
    user_stat = {
        "total": 1,
        "activeMonth": 1,
        "activeHalfyear": 1,
    }

    return {
        "metadata": {},
        "openRegistrations": False,
        "protocols": ["activitypub"],
        "services": {"inbound": [], "outbound": []},
        "software": {"name": "cattle-grid", "version": "0.2.0"},
        "usage": {"users": user_stat},
        "version": "2.0",
    }
