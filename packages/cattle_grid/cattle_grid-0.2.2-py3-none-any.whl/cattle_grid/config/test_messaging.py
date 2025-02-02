from faststream.rabbit import RabbitExchange, RabbitBroker

from .messaging import exchange, internal_exchange, broker


def test_internal_exchange():
    result = internal_exchange()

    assert isinstance(result, RabbitExchange)


def test_exchange():
    result = exchange()

    assert isinstance(result, RabbitExchange)


def test_broker():
    broker1 = broker()
    broker2 = broker()

    assert broker1 == broker2
    assert isinstance(broker1, RabbitBroker)
