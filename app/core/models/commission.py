from sqlalchemy import Column, Integer, String, Float, Date
from app.core.database.base import Base


class Commission(Base):
    __tablename__ = "commissions"

    id = Column(Integer, primary_key=True, index=True)
    distributor_id = Column(Integer, index=True)
    month = Column(String, index=True)
    year = Column(Integer, index=True)
    amount = Column(Float)
