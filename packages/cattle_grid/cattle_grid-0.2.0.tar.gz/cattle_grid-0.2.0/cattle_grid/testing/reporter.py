"""
Made as a tool to create reports from test runs
done using behave. Basically, a scenario is run, and a markdown file is created.

Currently recorded are the step, the scenario, messages
received on the `incoming.#` and `outgoing.#` routing keys
of the cattle_grid exchange.

Finally, fetch results from gateway are reported.
"""

import asyncio
import json
from contextlib import asynccontextmanager

from faststream import Context
from faststream.rabbit import RabbitExchange, ExchangeType, RabbitRouter, RabbitQueue

from cattle_grid.config.messaging import internal_exchange

from cattle_grid.account.router.exchange import device_exchange

exchange = RabbitExchange("reporting", type=ExchangeType.TOPIC)

router = RabbitRouter()


lock = asyncio.Lock()
current_file: str | None = None


@asynccontextmanager
async def current_file_handler(mode="a"):
    async with lock:
        with open(current_file, mode) as fp:
            yield fp


@router.subscriber(RabbitQueue("step_queue", routing_key="step"), exchange)
async def reporting_step(msg):
    """Reports the current step"""
    if not current_file:
        return

    async with current_file_handler() as fp:
        fp.writelines(["## " + msg.get("type") + ": " + msg.get("name") + "\n\n"])


@router.subscriber(RabbitQueue("scenario_queue", routing_key="scenario"), exchange)
async def reporting_scenario(msg):
    """Reports the scenario.

    Note every scenario is written to its own file in the `reports` directory."""
    scenario = msg.get("name")
    async with lock:
        global current_file
        scenario_alpha = "".join([x for x in scenario if x.isalpha()])
        current_file = f"reports/{scenario_alpha}.md"

    async with current_file_handler(mode="w") as fp:
        fp.writelines([f"#{scenario}\n\n"])


@router.subscriber(
    RabbitQueue("processing_reporting_in", routing_key="incoming.#"),
    internal_exchange(),
)
@router.subscriber(
    RabbitQueue("processing_reporting_out", routing_key="outgoing.#"),
    internal_exchange(),
)
async def reporting_incoming_outgoing(
    msg: dict,
    routing_key=Context("message.raw_message.routing_key"),
):
    """Records incoming and outgoing messages"""
    if not current_file:
        return
    async with current_file_handler() as fp:
        fp.writelines(
            [
                f"""

```json title="{routing_key}"
""",
                json.dumps(msg, indent=2),
                "\n```\n\n",
            ]
        )

    return {}


@router.subscriber(
    RabbitQueue("reporting_fetch_result", routing_key="receive.#"),
    device_exchange,
)
async def fetch_result_reporting(
    msg: dict,
    routing_key=Context("message.raw_message.routing_key"),
):
    """Records the result of performed fetch requests"""
    if not current_file:
        return
    if msg.get("action") != "fetch_result":
        return {}

    async with current_file_handler() as fp:
        fp.writelines(
            [
                f"""

```json title="{routing_key}"
""",
                json.dumps(msg, indent=2),
                "\n```\n\n",
            ]
        )

    return {}
