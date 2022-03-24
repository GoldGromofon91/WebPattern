import os
import pika
import random
import time
import requests

hostname = 'rabbitmq'
port = 5672

credentials = pika.PlainCredentials(username='myuser', password='mypassword')
parameters = pika.ConnectionParameters(host=hostname, port=port, credentials=credentials)
connection = pika.BlockingConnection(parameters)

# url = os.environ.get('rabbitmq', 'amqp://myuser:mypassword@rabbitmq:5672/%2f')
# # url = os.environ.get('localhost', 'amqp://myuser:mypassword@localhost:5672/%2f')
# params = pika.URLParameters(url)
# # params.socket_timeout = 5
# print(url)
# print(params)
# connection = pika.BlockingConnection(params)


channel = connection.channel()
channel.queue_declare(queue='repair')


def callback(ch, method, properties, body):
    """
    Обработка чтения из очереди
    """
    phone = body
    print('phone = ', body)
    # Начинаем процедуру ремонта
    repair_time = random.randint(3, 40)
    time.sleep(repair_time)
    # После окончания отправляем запрос на обновление статуса заказа
    print('Время ожидания: ', repair_time)
    print('Заказ готов')
    requests.post('http://flask_app:5000/change/', data={'phone': phone, 'status': 'DONE'})
    # requests.post('http://127.0.0.1:5000/change/', data={'phone': phone, 'status': 'DONE'})


channel.basic_consume(queue='repair', on_message_callback=callback)

print('start')
channel.start_consuming()
