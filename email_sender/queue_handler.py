import os
import sys

import pika

from .send_email import send_email


RABBIT_QUEUE = os.environ['RABBIT_QUEUE']

RABBITMQ_USER = os.environ['RABBITMQ_USER']
RABBITMQ_PASS = os.environ['RABBITMQ_PASS']
RABBITMQ_HOST = os.environ['RABBITMQ_HOST']
RABBITMQ_PORT = os.environ['RABBITMQ_PORT']


def queue_handler():
    try:
        connection = pika.BlockingConnection(
            pika.URLParameters(f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/")
        )
    except Exception as e:
        print("Connection error!")
        print(e)
        sys.exit(1)

    channel = connection.channel()

    # сохраняемая очередь
    channel.queue_declare(queue=RABBIT_QUEUE, durable=True)

    # не распределять новые задачи этому обработчику пока он не обработает текущую
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=RABBIT_QUEUE, on_message_callback=send_email)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
