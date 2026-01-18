import pika
import json
import os
import time


RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")

def publish_event(routing_key, message):
    """Wysyła wiadomość do Exchange 'take_n_watch_events'"""
    connection = None
    retries = 5
    

    while retries > 0:
        try:
            params = pika.URLParameters(RABBITMQ_URL)
            connection = pika.BlockingConnection(params)
            break
        except pika.exceptions.AMQPConnectionError:
            retries -= 1
            print(f" [!] RabbitMQ nie odpowiada. Próba ponownego połączenia... (Zostało: {retries})")
            time.sleep(3)
    
    if not connection:
        print(" [X] Błąd: Nie udało się połączyć z RabbitMQ.")
        return

    try:
        channel = connection.channel()
        
        
        channel.exchange_declare(
            exchange='take_n_watch_events', 
            exchange_type='topic', 
            durable=True
        )

        channel.basic_publish(
            exchange='take_n_watch_events',
            routing_key=routing_key,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  
            )
        )
        
        print(f" [v] Pomyślnie wysłano zdarzenie '{routing_key}'")
        
    except Exception as e:
        print(f" [X] Błąd podczas publikowania zdarzenia: {e}")
    finally:
        if connection and not connection.is_closed:
            connection.close()