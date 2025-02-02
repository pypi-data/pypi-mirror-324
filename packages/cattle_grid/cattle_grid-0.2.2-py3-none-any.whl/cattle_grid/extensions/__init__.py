from pydantic import BaseModel
from fast_depends import Depends
from typing import Callable, Dict, Awaitable, List, Annotated, Any
from dataclasses import dataclass, field

from faststream.rabbit import RabbitRouter
from fastapi import APIRouter

from cattle_grid.config.messaging import exchange
from cattle_grid.model.extension import MethodInformation

from .util import skip_method_information


class BaseConfig(BaseModel): ...


@dataclass
class Extension:
    """Data model for an extension"""

    name: str
    """name of the extension, must be unique"""

    module: str
    """module the extension is defined in, should be set to `__name__`"""

    lifespan: Callable[[], Awaitable[None]] | None = None
    """The lifespan function"""

    config_class: Any = BaseConfig
    """Expected configuration class"""

    Config: Any | None = None
    """Annotation to retrieve the configuration, e.g.

    ```python
    @extension.lookup()
    async def lookup(
        lookup: Lookup, config: extension.Config
    ) -> Lookup: ...
    ```
    """
    configuration: Any | None = None

    activity_router: RabbitRouter = field(default_factory=RabbitRouter)
    api_router: APIRouter = field(default_factory=APIRouter)
    api_prefix: str = ""

    transformer: Callable[[Dict], Awaitable[Dict]] | None = None
    transformer_inputs: List[str] | None = None
    transformer_outputs: List[str] | None = None

    lookup_method: Callable[[str], Awaitable[Dict]] | None = None
    lookup_order: int | None = None

    method_information: List[MethodInformation] = field(default_factory=list)

    def __post_init__(self):
        def get_config():
            return self.configuration

        self.Config = Annotated[self.config_class, Depends(get_config)]

    def configure(self, config: dict):
        """Configures the extension

        The configuration is validated using the config_class.
        """
        self.configuration = self.config_class.model_validate(config)

    def transform(self, inputs: List[str] = [], outputs: List[str] = []):
        """Allows building the extension via decorator. Usage:

        ```python
        extension = Extension("my extension")

        @extension.transform(inputs=["inputs"], outputs=["outputs"])
        async def transformer(a: dict):
            ...
        ```
        """
        if self.transformer:
            raise ValueError("You should not override an existing transformer")

        def inner(func):
            self.transformer = func
            self.transformer_inputs = inputs
            self.transformer_outputs = outputs

            return func

        return inner

    def subscribe(self, routing_key: str, description: str | None = None):
        """Allows building the extension via decorator.

        ```python
        extension = Extension("my extension")

        @extension.subscribe("routing_key")
        async def subscriber(msg: dict): ...
        ```

        Dependency injection is available for the subscriber function.
        """

        def inner(func):
            if description is None:
                function_description = func.__doc__
            else:
                function_description = description

            self.activity_router.subscriber(
                routing_key, exchange=exchange(), title=routing_key
            )(func)

            if not skip_method_information(routing_key):

                self.method_information.append(
                    MethodInformation(
                        module=self.module,
                        routing_key=routing_key,
                        description=function_description,
                    )
                )

            return func

        return inner

    def lookup(self):
        """Allows building the extension via decorator.

        ```python
        extension = Extension("my extension")

        @extension.lookup()
        async def lookup(l: Lookup) -> Lookup:
            ...
        ```
        Dependency injection is available for the lookup function.
        """

        def inner(func):
            self.lookup_method = func
            return func

        return inner

    def get(self, path):
        """Allows one to add a get endpoint to the API Router
        of the extension

        """

        def inner(func):
            self.api_router.get(path)(func)
            return func

        return inner
