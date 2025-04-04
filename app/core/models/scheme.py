from sqlalchemy import Column, Integer, String
from app.core.database.base import Base

class Scheme(Base):
    __tablename__ = "schemes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    category = Column(String)
    fund_house = Column(String)
