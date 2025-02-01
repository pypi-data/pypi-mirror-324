import click

from faststream import FastStream
from faststream.rabbit import RabbitBroker
from faststream.asyncapi import get_app_schema

from .load import load_extension


def schema_for_extension(extension):
    broker = RabbitBroker()
    broker.include_router(extension.activity_router)

    app = FastStream(broker, title=extension.name)

    return get_app_schema(app)


def add_extension_commands(main):
    @main.group()
    def extensions(): ...

    @extensions.command()
    @click.argument("module")
    def async_api(module):
        extension = load_extension({"module": module})
        name = extension.name.replace(" ", "_")
        schema = schema_for_extension(extension).to_json()

        with open(f"./docs/assets/schemas/asyncapi_{name}.json", "w") as fp:
            fp.write(schema)
