import pika
import json
from class_types import Endpoint
import requests

#connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
#channel = connection.channel()
endpoints = {}
with open("endpoints.json") as endpoints_config:
    data = json.load(endpoints_config)
    for idx,ep in enumerate(data['services']):
        endpoints[ep['domain']] = Endpoint(ep['domain'],ep['ip'],ep['port'])

to = 'mpcs.uchicago.51205@gmail.com' # send it to itself
dummy_email = {'to':to,'subject':'Holiday Wish from Team 3', 'body':'Happy Thanksgiving !'}
headers = {'Content-Type':'application/json'}
#channel.queue_declare(queue='email_queue')
#channel.basic_publish(exchange='',
#                      routing_key='email_queue',
#                      body=json.dumps(dummy_email))
r= requests.post(endpoints['mediator'].get_prefix() + "send_email", data=json.dumps(dummy_email),headers=headers)
print(r.json(),r.status_code)
print(" [x] Sent 'dummy email!'")
#connection.close()


