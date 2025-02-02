"""
Helper class to create documentation for the API

"""

from fastapi import FastAPI
from . import router

tags_description = [
    {
        "name": "actor",
        "description": """These functions provide the ability
to perform actions as an actor. This means interacting with
the Fediverse.

We remind the reader here that every account can have
multiple actors. The actor is usual indicated with
the `actorId` parameter.""",
    }
]

app = FastAPI(
    title="Account API for cattle_grid",
    description="""
This API is used to manage accounts, create actors,
manage actors, and perform actions as an actor.

Basically, it lets you control cattle_grid without using
the asynchronous API.
""",
    openapi_tags=tags_description,
)
app.include_router(router)
