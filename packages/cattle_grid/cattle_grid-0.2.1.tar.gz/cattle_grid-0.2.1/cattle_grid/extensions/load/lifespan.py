from contextlib import asynccontextmanager
from typing import List, AsyncContextManager
from fast_depends import inject

from cattle_grid.extensions import Extension


def collect_lifespans(extensions: List[Extension]) -> List[AsyncContextManager]:
    return [extension.lifespan for extension in extensions if extension.lifespan]


@asynccontextmanager
async def iterate_lifespans(lifespans: List[AsyncContextManager]):
    if len(lifespans) == 0:
        yield
        return

    async with inject(lifespans[0])():
        if len(lifespans) == 1:
            yield
        else:
            async with iterate_lifespans(lifespans[1:]):
                yield
