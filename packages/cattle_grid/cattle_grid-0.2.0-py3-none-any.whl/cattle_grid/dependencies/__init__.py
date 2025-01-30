"""Dependencies injected by fast_depends"""

import aiohttp
import logging

from typing import Annotated, Callable, Awaitable, Dict, List
from fast_depends import Depends
from faststream import Context
from faststream.rabbit import RabbitExchange

from sqlalchemy.ext.asyncio import AsyncEngine

from cattle_grid.model.lookup import LookupMethod
from cattle_grid.model.extension import MethodInformation
from cattle_grid.config.messaging import exchange

from .globals import get_transformer, get_lookup, get_engine, get_method_information

logger = logging.getLogger(__name__)


#
# This seems hacky to ensure only one session exists ...
#
session: aiohttp.ClientSession | None = None


async def get_client_session():
    global session

    if session is None:
        async with aiohttp.ClientSession() as cs:
            logger.warning(
                "Using new aiohttp session. Set one to the global session to avoid this."
            )
            yield cs
    else:
        yield session


ClientSession = Annotated[aiohttp.ClientSession, Depends(get_client_session)]
"""The [aiohttp.ClientSession][] used by the application"""

Transformer = Annotated[Callable[[Dict], Awaitable[Dict]], Depends(get_transformer)]
"""The transformer loaded from extensions"""

LookupAnnotation = Annotated[LookupMethod, Depends(get_lookup)]
"""The lookup method loaded from extensions"""

ActivityExchange = Annotated[RabbitExchange, Depends(exchange)]
"""The activity exchange"""

SqlAsyncEngine = Annotated[AsyncEngine, Depends(get_engine)]
"""Returns the SqlAlchemy AsyncEngine"""

CorrelationId = Annotated[str, Context("message.correlation_id")]
"""The correlation id of the message"""

MethodInformation = Annotated[List[MethodInformation], Depends(get_method_information)]
"""Returns the information about the methods that are a part of the exchange"""
