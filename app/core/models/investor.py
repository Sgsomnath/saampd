from sqlalchemy import Column, Integer, String
from app.core.database.base import Base

class Investor(Base):
    __tablename__ = "investors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
