# log_service/db.py
from datetime import datetime
from pymongo import MongoClient

MONGO_URL = "mongodb://localhost:27017"
client = MongoClient(MONGO_URL)

db = client["video_rental_logs"]
qr_scans_collection = db["qr_scans"]


def log_qr_scan(qr_code: str, action: str, user_id: int | None, success: bool, message: str | None = None):
    """
    action: np. "CHECKOUT", "RETURN", "INVENTORY_CHECK"
    """
    doc = {
        "qr_code": qr_code,
        "action": action,
        "user_id": user_id,
        "success": success,
        "message": message,
        "timestamp": datetime.utcnow(),
    }
    qr_scans_collection.insert_one(doc)
