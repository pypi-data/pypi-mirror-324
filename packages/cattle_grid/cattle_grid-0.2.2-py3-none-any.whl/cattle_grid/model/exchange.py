from enum import StrEnum, auto
from pydantic import BaseModel, ConfigDict, Field
from typing import Dict, Any, List


class UpdateActionType(StrEnum):
    """Available actions for updating the actor"""

    add_identifier = auto()
    """Adds a new identifier"""
    update_identifier = auto()
    """Updates an identifer"""
    remove_identifier = auto()
    """Removes an identifier"""


class UpdateAction(BaseModel):
    """Action to update an actor"""

    model_config = ConfigDict(
        extra="allow",
    )

    action: UpdateActionType


class UpdateIdentifierAction(UpdateAction):
    """Used to update an identifier of the actor"""

    identifier: str
    primary: bool = Field(
        False,
        description="Set the identifier as the primary one, if the identifier corresponds to an acct-uri this will update the primary identifier",
    )


class UpdateActorMessage(BaseModel):
    """
    Allows one to update the actor object
    """

    # model_config = ConfigDict(
    #     extra="forbid",
    # )
    actor: str = Field(
        ...,
        examples=["http://local.example/actor"],
        description="""
    The URI of the actor being updated. Must be managed by cattle_grid
    """,
    )
    profile: Dict[str, Any] | None = Field(
        None,
        examples=[{"summary": "A new description of the actor"}],
        description="""
    New profile object for the actor. The fields.
    """,
    )
    autoFollow: bool | None = Field(
        None,
        examples=[True, False, None],
        description="""
    Enables setting actors to automatically accept follow requests
    """,
    )

    actions: List[UpdateAction] = Field(
        default_factory=list,
        description="""Actions to be taken when updating the profile""",
    )


class DeleteActorMessage(BaseModel):
    """
    Allows one to delete the actor object
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    actor: str = Field(
        ...,
        examples=["http://local.example/actor"],
        description="""
    The URI of the actor being deleted.
    """,
    )
