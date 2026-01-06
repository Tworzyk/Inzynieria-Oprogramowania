import pika
import json
import os

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")


def publish_event(routing_key, message):
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()
    channel.exchange_declare(exchange='take_n_watch_events', exchange_type='topic')

    channel.basic_publish(
        exchange='take_n_watch_events',
        routing_key=routing_key,
        body=json.dumps(message)
    )
    connection.close()