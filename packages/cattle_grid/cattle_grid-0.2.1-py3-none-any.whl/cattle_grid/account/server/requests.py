from pydantic import BaseModel, Field


class PerformRequest(BaseModel):
    """Request send to enqueue an action"""

    actor_id: str = Field(alias="actorId", examples=["http://actor.example/someId"])
    """The actor id, must be long to the account"""

    action: str = Field(examples=["send_message", "update_actor"])
    """The action to be performed. Corresponds to a routing_key on the ActivityExchange"""

    data: dict = Field(
        examples=[
            {
                "actorId": "http://actor.example/someId",
                "content": "mooo",
                "type": "AnimalSound",
                "to": ["http://other.example"],
            }
        ]
    )
    """Data corresponding to the action"""


class CreateActorRequest(BaseModel):
    """Used to create an actor for the account"""

    base_url: str = Field(
        alias="baseUrl",
        examples=["http://domain.example"],
        description="""Base url of the actor. The actor URI will be
    of the form `{baseUrl}/actor/some_secret`
    """,
    )
    """ """

    handle: str | None = Field(
        None,
        examples=["alice"],
        description="""If present, an acct-uri of the form `acct:{handle}@{domain}` where domain is determined from `baseUrl` is created""",
    )
    """ """
