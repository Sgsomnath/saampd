from sqlalchemy import Column, Integer, String
from app.core.database.base import Base

class Admin(Base):
    __tablename__ = "admins"
    __table_args__ = {"extend_existing": True}  # Prevent redefinition error

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
