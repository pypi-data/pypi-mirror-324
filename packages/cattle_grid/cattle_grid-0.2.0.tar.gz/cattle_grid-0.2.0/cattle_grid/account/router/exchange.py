from faststream.rabbit import RabbitExchange, ExchangeType

device_exchange = RabbitExchange("amq.topic", type=ExchangeType.TOPIC, durable=True)
