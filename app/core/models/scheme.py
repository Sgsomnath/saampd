from sqlalchemy import Column, Integer, String, Float
from app.core.database.base import Base

class Scheme(Base):
    __tablename__ = "schemes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    scheme_code = Column(String, nullable=False, unique=True, index=True)  # BSE/AMFI code
    category = Column(String, nullable=False)
    fund_house = Column(String, nullable=False)
    risk_level = Column(String, default="Moderate")  # e.g., Low, Moderate, High
    nav = Column(Float, default=0.0)                 # Latest NAV (Net Asset Value)
    plan_type = Column(String, default="Growth")     # Growth / Dividend

    def __repr__(self):
        return f"<Scheme(id={self.id}, name='{self.name}', code='{self.scheme_code}', category='{self.category}')>"
