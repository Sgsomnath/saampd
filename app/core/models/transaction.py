from sqlalchemy import Column, Integer, Float, ForeignKey
from app.core.database.base import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    investor_id = Column(Integer, ForeignKey("investors.id"))
