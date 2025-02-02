# Methods

As described in [Triggers](./cattle_drive.md#triggers), most user actions with `cattle_grid` can be described as executing a method.
This document describes the methods implemented in `cattle_grid`
additional methods can be implemented through [Extensions](./extensions/index.md).

## Defined methods

### `send_message`

Send a [cattle_grid.model.ActivityMessage][] to the `send_message` routing_key, and this will trigger a message being send. We note
that `cattle_grid` will send the content as is, so nothing like
assigning an `id` will happen. The process after a `send_message`
looks roughly as follows:

- The type of the activity is determined
- The raw activity is published to the routing key `outgoing.type` on the RawExchange.
- This triggers the message being send to its recipients, and the raw exchange actions.
- The activity is transformed and published to `outgoing.type` on the ActivityExchange.
- The activity will be forwarded to `receive.AccountName.outgoing`.
- Possible extensions are triggered.

### `update_actor`

Actors are updated by sending a [cattle_grid.model.exchange.UpdateActorMessage][] message to the `update_actor` routing_key.

The possible actions are described by the [cattle_grid.model.exchange.UpdateActionType][] enum.

- [cattle_grid.model.exchange.UpdateIdentifierAction][]: Used to update identifiers

### `delete_actor`

This is simple, send a [cattle_grid.model.exchange.DeleteActorMessage][]
to the `delete_actor` routing_key, and the actor contained in the message
will be deleted.

!!! warning
    The meaning of deleted is somewhat vague here. This method for now,
    triggers a delete activity being send out, and marks the actor as
    deleted. This means that deleting the actor, and its data will occur
    later.

## Description in the code

The methods are described by [cattle_grid.exchange.info.exchange_method_information][] and can be queried through
requesting `info` through CattleDrive.

!!! info
    Requesting the methods through `info` also returns information
    on methods defined through extensions.
