from typing import List
from pydantic import BaseModel, Field, ConfigDict


class SignInData(BaseModel):
    name: str
    password: str


class SignUpData(BaseModel):
    name: str
    password: str


class TokenResponse(BaseModel):
    token: str


class LookupRequest(BaseModel):
    actor_id: str = Field(alias="actorId")
    uri: str


class LookupResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    raw: dict


class DeleteActorRequest(BaseModel):
    actor_id: str = Field(alias="actorId")


class PublicIdentifierInformation(BaseModel):
    identifier: str
    name: str
    preference: int


class ActorInformationRequest(BaseModel):
    actor_id: str = Field(alias="actorId")
    update: dict | None = None


class ActorInformationResponse(BaseModel):
    raw: dict
    identifiers: List[PublicIdentifierInformation] = Field(default_factory=list)
    automatically_accept_followers: bool = False


class SettingsResponse(BaseModel):
    base_urls: List[str] = Field(
        default_factory=list,
        examples=["http://domain.example"],
        serialization_alias="baseUrls",
    )
