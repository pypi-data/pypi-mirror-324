from functools import lru_cache

from faststream.rabbit import RabbitExchange, RabbitBroker, ExchangeType

from .settings import get_settings


@lru_cache
def internal_exchange(settings=get_settings()) -> RabbitExchange:
    """The internal exchange used to process
    ActivityPub messages related to the social graph

    :returns:
    """
    return RabbitExchange(
        settings.activity_pub.internal_exchange, type=ExchangeType.TOPIC
    )


@lru_cache
def exchange(settings=get_settings()) -> RabbitExchange:
    """Returns the public exchange used to process

    :returns:
    """
    return RabbitExchange(settings.activity_pub.exchange, type=ExchangeType.TOPIC)


@lru_cache
def account_exchange(settings=get_settings()) -> RabbitExchange:
    """Returns the exchange used to distribute messages between accounts

    :returns:
    """
    durable = True if settings.activity_pub.account_exchange == "amq.topic" else False

    return RabbitExchange(
        settings.activity_pub.account_exchange, type=ExchangeType.TOPIC, durable=durable
    )


current_broker: RabbitBroker | None = None


def broker(settings=get_settings()) -> RabbitBroker:
    """Returns the rabbitmq broker

    :returns:
    """
    global current_broker

    if current_broker is None:
        current_broker = RabbitBroker(settings.amqp_uri)

    return current_broker
