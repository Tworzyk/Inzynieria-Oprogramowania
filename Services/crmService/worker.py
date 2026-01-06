import pika, json, os
from common import SessionLocal, engine, Base
from .models import CustomerLoyalty

Base.metadata.create_all(bind=engine)


def callback(ch, method, properties, body):
    data = json.loads(body)
    user_id = data['user_id']

    db = SessionLocal()
    customer = db.query(CustomerLoyalty).filter_by(user_id=user_id).first()

    if not customer:
        customer = CustomerLoyalty(user_id=user_id, points=0)
        db.add(customer)

    # Dodaj 10 punktów za każde wypożyczenie (Logika CRM)
    customer.points += 10.0
    db.commit()
    db.close()
    print(f" [CRM] Zaktualizowano punkty dla użytkownika {user_id}")


# Start nasłuchiwania kolejek
def run_worker():
    url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")
    connection = pika.BlockingConnection(pika.URLParameters(url))
    channel = connection.channel()
    channel.queue_declare(queue='crm_queue')
    channel.queue_bind(exchange='take_n_watch_events', queue='crm_queue', routing_key='rental.created')
    channel.basic_consume(queue='crm_queue', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


if __name__ == "__main__":
    run_worker()