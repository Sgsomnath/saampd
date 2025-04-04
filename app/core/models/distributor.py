# app/core/models/distributor.py

from sqlalchemy import Column, Integer, String
from app.core.database.base import Base

class Distributor(Base):
    __tablename__ = "distributors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
