import os

import pika

from .send_email import send_email


QUEUE_NAME = 'mail_processed'
EXCHANGE_NAME = 'logs'

RABBITMQ_USER = os.environ['RABBITMQ_USER']
RABBITMQ_PASS = os.environ['RABBITMQ_PASS']
RABBITMQ_HOST = os.environ['RABBITMQ_HOST']
RABBITMQ_PORT = os.environ['RABBITMQ_PORT']


def queue_handler():
    connection = pika.BlockingConnection(
        pika.URLParameters(f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/")
    )
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='fanout')

    # сохраняемая очередь
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    # привязать очередь к распределителю X
    channel.queue_bind(exchange='logs', queue=QUEUE_NAME)

    # не распределять новые задачи этому обработчику пока он не обработает текущую
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=send_email)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
