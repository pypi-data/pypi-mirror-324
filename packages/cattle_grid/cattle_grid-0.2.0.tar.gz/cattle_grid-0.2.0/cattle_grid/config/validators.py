from dynaconf import Validator

base_validators = [
    Validator("amqp_uri", default="amqp://localhost"),
    Validator("db_uri", default="sqlite://cattle_grid.db"),
    Validator("enable_reporting", cast=bool, default=False),
]
"""Validates the basic configuration"""

activity_pub_validators = [
    Validator("activity_pub.internal_exchange", default="cattle_grid_internal"),
    Validator("activity_pub.exchange", default="cattle_grid"),
]
"""Validators for ActivityPub"""

gateway_admin_validations = [
    Validator("gateway.admin.enable", cast=bool, default=False),
    Validator("gateway.admin.enable_reset", cast=bool, default=False),
]
"""Validators for the gateway"""


plugins_validations = [
    Validator("plugins", default=lambda a, b: list([]), cast=list),
]
"""Validators for the plugins"""


frontend_validations = [
    Validator(
        "frontend.base_urls",
        default=lambda a, b: list([]),
        cast=lambda x: [str(y) for y in x],
        condition=lambda items: all(
            x.startswith("http://") or x.startswith("https://") for x in items
        ),
    )
]
"""Validators for the frontend"""


extensions_validations = [
    Validator("extensions", default=lambda a, b: list([]), cast=list),
]
"""Validators for the plugins"""

all_validators = (
    base_validators
    + activity_pub_validators
    + gateway_admin_validations
    + plugins_validations
    + frontend_validations
    + extensions_validations
)
