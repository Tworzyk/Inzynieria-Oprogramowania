from sqlalchemy import Column, Integer, DateTime, Numeric, Enum
from sqlalchemy.sql import func
from common.sql_db import Base
import enum

class RentalStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    LATE = "LATE"
    CANCELED = "CANCELED"

class Rental(Base):
    __tablename__ = "rentals"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    inventory_item_id = Column(Integer, nullable=False)
    rented_at = Column(DateTime, server_default=func.now())
    price = Column(Numeric(10, 2), nullable=False)
    status = Column(Enum(RentalStatus), default=RentalStatus.ACTIVE)