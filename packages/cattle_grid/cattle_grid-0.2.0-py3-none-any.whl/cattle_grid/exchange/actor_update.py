import logging

from cattle_grid.activity_pub.models import Actor, PublicIdentifier

from cattle_grid.model.exchange import (
    UpdateAction,
    UpdateActionType,
    UpdateIdentifierAction,
)

logger = logging.getLogger(__name__)


def find_identifier(actor: Actor, to_find: str) -> PublicIdentifier | None:
    for identifier in actor.identifiers:
        if identifier.identifier == to_find:
            return identifier
    return None


def new_primary_preference(actor):
    return max(identifier.preference for identifier in actor.identifiers) + 1


async def handle_actor_update(actor: Actor, update: dict) -> None:
    action = update.get("action")

    if action == "addIdentifier":
        identifier = update.get("identifier")
        primary = update.get("primary")
        preference = 0

        if primary:
            preference = new_primary_preference(actor)

        await PublicIdentifier.create(
            actor=actor, identifier=identifier, name="fromweb", preference=preference
        )
    if action == "makePrimary":
        identifier = update.get("identifier", "")
        public_identifier = find_identifier(actor, identifier)
        if public_identifier is None:
            raise ValueError("Identifier not found")
        public_identifier.preference = new_primary_preference(actor)
        await public_identifier.save()
    if action == "setAutoFollow":
        actor.automatically_accept_followers = update.get("value", False)
        await actor.save()

    await actor.refresh_from_db()
    await actor.fetch_related("identifiers")


async def handle_actor_action(actor: Actor, action: UpdateAction) -> None:
    match action.action:
        case UpdateActionType.add_identifier:
            # FIXME: Need way to validate identifiers

            logger.info(action)

            # check if identifier already exists ...

            action = UpdateIdentifierAction.model_validate(action.model_dump())
            preference = 0

            if action.primary:
                preference = new_primary_preference(actor)

            await PublicIdentifier.create(
                actor=actor,
                identifier=action.identifier,
                name="through_exchange",
                preference=preference,
            )

            return True
        case UpdateActionType.update_identifier:
            await actor.fetch_related("identifiers")
            public_identifier = find_identifier(actor, action.identifier)
            if public_identifier is None:
                raise ValueError("Identifier not found")

            if action.primary:
                public_identifier.preference = new_primary_preference(actor)
            await public_identifier.save()

            return True

    return False
