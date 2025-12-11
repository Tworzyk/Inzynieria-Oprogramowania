# inventory_service/models.py
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Enum,
    DateTime,
    Boolean,
    UniqueConstraint,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from common.sql_db import Base

class CopyStatus(str, enum.Enum):
    AVAILABLE = "AVAILABLE"
    RENTED = "RENTED"
    LOST = "LOST"
    DAMAGED = "DAMAGED"

class InventoryItem(Base):
    __tablename__ = "inventory_items"
    __table_args__ = (
        UniqueConstraint("qr_code", name="uq_inventory_qr_code"),
    )

    id = Column(Integer, primary_key=True, index=True)

    # ID filmu z serwisu movie_service (w mikroserwisach możesz mieć inne ID,
    # tu zakładamy proste integerowe powiązanie)
    movie_id = Column(Integer, nullable=False, index=True)

    # Kod QR jako string (np. UUID, lub zakodowany JSON/URI)
    qr_code = Column(String(255), nullable=False, index=True)

    # lokalizacja fizyczna, np. "REGAL_A_03"
    location = Column(String(255), nullable=True)

    status = Column(
        Enum(CCopyStatus := CopyStatus, name="copy_status_enum"),
        nullable=False,
        default=CopyStatus.AVAILABLE,
    )

    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
