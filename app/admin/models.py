# app/admin/models.py

from sqlalchemy import Column, Integer, String
from app.core.database.base import Base  # Make sure this path is correct

class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
