from sqlalchemy import Column, Integer, Float
from common import Base

class CustomerLoyalty(Base):
    __tablename__ = "customer_loyalty"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, index=True)
    points = Column(Float, default=0.0)