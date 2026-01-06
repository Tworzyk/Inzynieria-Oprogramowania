from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from common.sql_db import get_db, engine, Base
from common.messaging import publish_event
from .models import Rental

Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.post("/rentals/")
def rent_movie(user_id: int, item_id: int, price: float, db: Session = Depends(get_db)):
    new_rental = Rental(user_id=user_id, inventory_item_id=item_id, price=price)
    db.add(new_rental)
    db.commit()

    # POWIADOMIENIE CRM PRZEZ RABBITHQ
    event = {"user_id": user_id, "item_id": item_id, "action": "NEW_RENTAL"}
    publish_event("rental.created", event)

    return {"status": "Rental created", "id": new_rental.id}