from sqlalchemy.orm import Session
from sqlalchemy import select

from Services.crmService.models import CustomerLoyalty
from Services.inventoryService.inventoryservice import InventoryItem, CopyStatus





def create_inventory_item(db: Session, movie_id: int, qr_code: str, location: str = None):
    """Tworzy nowy egzemplarz filmu w inwentarzu."""
    db_item = InventoryItem(
        movie_id=movie_id,
        qr_code=qr_code,
        location=location,
        status=CopyStatus.AVAILABLE
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_item_by_id(db: Session, item_id: int):
    """Pobiera konkretny egzemplarz po jego ID."""
    return db.query(InventoryItem).filter(InventoryItem.id == item_id).first()

def get_item_by_qr_code(db: Session, qr_code: str):
    """Pobiera egzemplarz na podstawie skanu kodu QR."""
    return db.query(InventoryItem).filter(InventoryItem.qr_code == qr_code).first()

def get_all_items_for_movie(db: Session, movie_id: int):
    """Pobiera wszystkie fizyczne kopie przypisane do danego filmu."""
    return db.query(InventoryItem).filter(InventoryItem.movie_id == movie_id).all()

def get_available_copies(db: Session, movie_id: int):
    """Pobiera tylko dostępne (nie wypożyczone) kopie danego filmu."""
    return db.query(InventoryItem).filter(
        InventoryItem.movie_id == movie_id,
        InventoryItem.status == CopyStatus.AVAILABLE,
        InventoryItem.is_active == True
    ).all()



def update_item_status(db: Session, item_id: int, new_status: CopyStatus):
    """Zmienia status egzemplarza (np. na RENTED po wypożyczeniu)."""
    db_item = get_item_by_id(db, item_id)
    if db_item:
        db_item.status = new_status
        db.commit()
        db.refresh(db_item)
    return db_item

def move_item_to_location(db: Session, item_id: int, new_location: str):
    """Aktualizuje lokalizację fizyczną egzemplarza w magazynie."""
    db_item = get_item_by_id(db, item_id)
    if db_item:
        db_item.location = new_location
        db.commit()
        db.refresh(db_item)
    return db_item

def deactivate_item(db: Session, item_id: int):

    db_item = get_item_by_id(db, item_id)
    if db_item:
        db_item.is_active = False
        db.commit()
    return db_item


def add_loyalty_points(db: Session, user_id: int, points_to_add: float):
    """Dodaje punkty lojalnościowe użytkownikowi (tworzy rekord jeśli nie istnieje)."""
    loyalty = db.query(CustomerLoyalty).filter(CustomerLoyalty.user_id == user_id).first()

    if not loyalty:
        loyalty = CustomerLoyalty(user_id=user_id, points=points_to_add)
        db.add(loyalty)
    else:
        loyalty.points += points_to_add

    db.commit()
    db.refresh(loyalty)
    return loyalty