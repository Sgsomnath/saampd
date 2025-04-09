from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.core.database.base import Base

class Investor(Base):
    __tablename__ = "investors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    mobile = Column(String, nullable=False)
    pan = Column(String, unique=True, nullable=True)  # PAN for KYC
    kyc_status = Column(String, default="Pending")    # e.g., Pending, Verified
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
