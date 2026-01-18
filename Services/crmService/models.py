from sqlalchemy import Column, Integer, Float
from Services.common.basesql import Base

class CustomerLoyalty(Base):
    __tablename__ = "customer_loyalty"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, index=True)
    points = Column(Integer, default=0)