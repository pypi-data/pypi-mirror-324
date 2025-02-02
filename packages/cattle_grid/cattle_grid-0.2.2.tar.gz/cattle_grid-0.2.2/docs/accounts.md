# Accounts in cattle_grid

The basic level of access control provided by
cattle_grid is base on accounts. Each account has a
__name__ and a __password__, and these are used for
authentication, e.g. when [connecting to RabbitMQ](reference/rabbitmq.md).

Once you have an account, you are able to:

- Obtain information about the backend and your actors
- Create new actors
- Perform actions as your actor, including updating, deleting, and fetching Fediverse resources.

Currently, there are few restrictions, except that the
actor must belong to the account. This is planned to change.

## Managing accounts

### Creating an account

An account can currently be created via the command line

```bash
python -mcattle_grid account new NAME PASSWORD
```

### Listing accounts

This can be done via the command line

```bash
python -mcattle_grid account list
```

## Configuration

Configuration for accounts is under the `account` key. Default values
and configuration names can be found in
[cattle_grid.config.validators.account_validations][].

!!! warning
    I'm unsure what would happen if one allows many special characters
    in the account name. This is due to the account name being
    used as part of a routing_key, e.g. `receive.Alice.incoming`.
    For example, allowing a dot `.` in the account name would
    break certain parts of the logic.
