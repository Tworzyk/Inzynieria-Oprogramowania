# rental_service/models.py
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    Numeric,
    Enum,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from common.sql_db import Base


class RentalStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    LATE = "LATE"
    CANCELED = "CANCELED"


class Rental(Base):
    __tablename__ = "rentals"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, nullable=False, index=True)           # z user_service
    inventory_item_id = Column(Integer, nullable=False, index=True) # z inventory_service

    rented_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    due_at = Column(DateTime(timezone=True), nullable=False)  # termin oddania
    returned_at = Column(DateTime(timezone=True), nullable=True)

    status = Column(Enum(RentalStatus, name="rental_status_enum"), nullable=False, default=RentalStatus.ACTIVE)

    price = Column(Numeric(10, 2), nullable=False)       # cena standardowa
    late_fee_total = Column(Numeric(10, 2), nullable=False, default=0)  # naliczone kary

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
