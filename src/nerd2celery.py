import pika
import json
import uuid
import datetime
import sys
import os
from collections import deque

### SKRIPT PRO KONTROLU COMMANDU PRO NAGIOS

# skript inicializuje promenne, pripoji se k RabbitMQ a odebira zpravy, zapisuje do tmp souboru 
# testuje z tmp souboru, kdy naposledy dobehlo OK, vrati vysledek suitable pro Nagios

true = True


class Monitor:
    def __init__(self, *args, **kwargs):
    
        self.username = 'guest'
        self.password = 'guest'
        self.host = 'localhost'
        self.port = 5672
        self.vhost = '/'
        self.queue = 'idea-nerd2grip'
        self.cmdlog_id = ''
        self.tmpfile = '/tmp/soubor'

        
    def callback(self, ch, method, properties, body):
        msg = str(body, 'utf-8')
        self.add(msg) 
            
    #def end_consuming(self):
        #self.channel.stop_consuming()
        #self.connection.close()      
   
        
    def connect(self):
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(self.host,
                                               self.port,
                                               self.vhost,
                                               credentials)
        self.connection = pika.BlockingConnection(parameters)          
        self.channel = self.connection.channel()
        #self.channel.queue_declare(queue=self.queue, durable=True)             
        #self.connection.add_timeout(deadline=5, callback_method=self.end_consuming)
        
        try:
            self.channel.basic_consume(self.callback,
                              queue=self.queue,
                              no_ack=True)
            self.channel.start_consuming()  
        
        except KeyboardInterrupt:
            self.channel.stop_consuming()
            self.connection.close()
            
    
    def add(self, idea):
        credentials = pika.PlainCredentials('guest', 'guest')
        parameters = pika.ConnectionParameters('localhost',
                                               5672,
                                               '/',
                                               credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        
        channel.basic_publish(exchange='celery',
                              routing_key='celery',
                              body='{"task": "add", "id": "' + str(uuid.uuid4()) + '", "args": [' + json.dumps(idea) + '], "kwargs": {}}',
                              properties=pika.BasicProperties(content_type='application/json'))
        
        connection.close()        
            
            
    

instance = Monitor()
instance.connect()

