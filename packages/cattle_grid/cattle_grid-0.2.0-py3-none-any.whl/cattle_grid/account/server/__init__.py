import logging

from uuid import uuid4
from typing import Annotated, Any
from fastapi import APIRouter, HTTPException, Depends

from cattle_grid.config.settings import get_settings

from cattle_grid.account.models import AuthenticationToken
from cattle_grid.account.account import account_with_username_password


from .responses import TokenResponse, SignInData, SettingsResponse
from .dependencies import CurrentAccount
from .actor import actor_router
from .account import account_router

logger = logging.getLogger(__name__)


router = APIRouter()
router.include_router(actor_router)
router.include_router(account_router)


@router.post("/signin")
async def signin(data: SignInData) -> TokenResponse:
    account = await account_with_username_password(data.name, data.password)
    if account is None:
        raise HTTPException(401)

    token = str(uuid4())
    await AuthenticationToken.create(account=account, token=token)

    return TokenResponse(token=token)


# @router.post("/signup", tags=["account_auth"])
# async def signup(data: SignUpData):
#     await create_account(data.name, data.password)
#     return


@router.get("/settings")
async def return_settings(
    account: CurrentAccount, settings: Annotated[Any, Depends(get_settings)]
) -> SettingsResponse:
    return SettingsResponse(
        base_urls=settings.frontend.base_urls,
    )
