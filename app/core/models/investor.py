from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.core.database.base import Base

class Investor(Base):
    __tablename__ = "investors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    mobile = Column(String, nullable=False)
    dob = Column(String, nullable=True)                      # ✅ নতুন ফিল্ড
    pan = Column(String, unique=True, nullable=True)
    kyc_status = Column(String, default="Pending")
    fatca_status = Column(String, default="Pending")         # ✅ নতুন ফিল্ড
    nomination_status = Column(String, default="Not Added")  # ✅ নতুন ফিল্ড
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
