import time
import os
from sqlalchemy.exc import ProgrammingError, OperationalError

# 1. Poprawione importy - używamy pełnej ścieżki Services...
from Services.common.basesql import SessionLocal, engine, Base
from Services.crmService.models import CustomerLoyalty
from Services.inventoryService.crud import create_inventory_item, update_item_status
from Services.inventoryService.inventoryservice import InventoryItem, CopyStatus
from Services.common.messaging import publish_event

def wait_for_db():
    """Funkcja czekająca na gotowość bazy danych"""
    retries = 15
    while retries > 0:
        try:
            # Próbujemy nawiązać realne połączenie
            conn = engine.connect()
            conn.close()
            return True
        except Exception:
            print(f"Oczekiwanie na bazę danych... (Pozostało prób: {retries})")
            time.sleep(3)
            retries -= 1
    return False

def main():
    if not wait_for_db():
        print("Błąd: Nie można połączyć się z bazą danych.")
        return

    # 2. Bezpieczna inicjalizacja tabel (odporna na DuplicateTable)
    print("Inicjalizacja tabel w bazie danych...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Tabele zostały pomyślnie zainicjalizowane.")
    except (ProgrammingError, OperationalError) as e:
        if "already exists" in str(e):
            print("Tabele/Indeksy już istnieją, kontynuuję...")
        else:
            print(f"Błąd podczas tworzenia tabel: {e}")

    db = SessionLocal()

    try:
        print("\n" + "=" * 50)
        print("   INVENTORY SERVICE - NOWE WYPOŻYCZENIE")
        print("=" * 50)

        
        user_id = 10
        movie_id = 110

        unique_qr = f"QR-DOCKER-{int(time.time())}"
        nowy_film = create_inventory_item(
            db=db,
            movie_id=movie_id,
            qr_code=unique_qr,
            location="REGAL_DOCKER"
        )
        print(f"1. Dodano film do bazy: ID={nowy_film.id}, QR={unique_qr}")

        
        update_item_status(db=db, item_id=nowy_film.id, new_status=CopyStatus.RENTED)
        print(f"2. Zmieniono status na RENTED")

      
        event_data = {
            "user_id": user_id,
            "movie_id": movie_id,
            "item_id": nowy_film.id,
            "timestamp": time.time()
        }

        print(f"3. Wysyłanie zdarzenia 'rental.created' dla UserID: {user_id}...")
        publish_event(routing_key='rental.created', message=event_data)
        print("   [Okey] Zdarzenie wysłane do RabbitMQ.")

        
        print("\n" + "=" * 50)
        print("          AKTUALNY STAN BAZY (WIDOK Z INVENTORY)")
        print("=" * 50)

        items = db.query(InventoryItem).all()
        print(f"{'ID':<4} | {'MOVIE':<6} | {'QR_CODE':<15} | {'STATUS':<10}")
        print("-" * 45)
        for i in items:
            s = i.status.value if hasattr(i.status, 'value') else i.status
            print(f"{i.id:<4} | {i.movie_id:<6} | {i.qr_code:<15} | {s:<10}")

        
        print("\nCzekam 3 sekundy na aktualizację punktów przez Workera...")
        time.sleep(3)

        print("\n[TABELA: CUSTOMER_LOYALTY (Aktualizowana przez Workera)]")
        loyalty = db.query(CustomerLoyalty).all()
        for l in loyalty:
            u_id = getattr(l, 'user_id', getattr(l, 'customer_id', 'N/A'))
            pts = getattr(l, 'points', getattr(l, 'loyalty_points', 'N/A'))
            print(f"User: {u_id} | Punkty: {pts}")

    except Exception as e:
        print(f"Wystąpił błąd w main: {e}")
    finally:
        db.close()
        print("\nZakończono pracę Inventory Service.")

if __name__ == "__main__":
    main()