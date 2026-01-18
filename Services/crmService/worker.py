import pika, json, os
from Services.common.basesql import SessionLocal, engine, Base
from Services.crmService.models import CustomerLoyalty
from Services.inventoryService.crud import add_loyalty_points

Base.metadata.create_all(bind=engine)

def callback(ch, method, properties, body):
    data = json.loads(body)
    user_id = data.get('user_id')
    db = SessionLocal()
    try:
        add_loyalty_points(db, user_id=user_id, points_to_add=10.0)
        print(f" [CRM] Dodano 10 pkt dla użytkownika {user_id}")
    finally:
        db.close()

def run():
    url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")
    connection = pika.BlockingConnection(pika.URLParameters(url))
    channel = connection.channel()
    channel.queue_declare(queue='crm_queue')
    channel.queue_bind(exchange='take_n_watch_events', queue='crm_queue', routing_key='rental.created')
    channel.basic_consume(queue='crm_queue', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == "__main__":
    run()