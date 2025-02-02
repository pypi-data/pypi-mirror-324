from tortoise import fields
from tortoise.models import Model


class Account(Model):
    """Represents an Account"""

    id = fields.IntField(primary_key=True)

    name = fields.CharField(max_length=255)
    """The account name"""

    password_hash = fields.CharField(max_length=255)
    """The hashed password"""

    actors: fields.ReverseRelation["ActorForAccount"]
    """Actors associated with this account"""

    token: fields.ReverseRelation["AuthenticationToken"]
    """Authentication tokens for this account"""


class ActorForAccount(Model):
    id = fields.IntField(primary_key=True)

    account: fields.ForeignKeyRelation[Account] = fields.ForeignKeyField(
        "gateway_models.Account", related_name="actors"
    )
    actor = fields.CharField(max_length=255)


class AuthenticationToken(Model):
    token = fields.CharField(max_length=64, primary_key=True)

    account: fields.ForeignKeyRelation[Account] = fields.ForeignKeyField(
        "gateway_models.Account", related_name="tokens"
    )
