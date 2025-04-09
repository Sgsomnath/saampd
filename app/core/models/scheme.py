from sqlalchemy import Column, Integer, String
from app.core.database.base import Base

class Scheme(Base):
    __tablename__ = "schemes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    category = Column(String, nullable=False)
    fund_house = Column(String, nullable=False)

    def __repr__(self):
        return f"<Scheme(id={self.id}, name='{self.name}', category='{self.category}', fund_house='{self.fund_house}')>"
