from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.core.database.base import Base

class Investor(Base):
    __tablename__ = "investors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    mobile = Column(String, nullable=False)
    date_of_birth = Column(String, nullable=True)  # Keeps the String format for now
    gender = Column(String, nullable=True)
    pan_number = Column(String, unique=True, nullable=True)
    aadhar_number = Column(String, unique=True, nullable=True)

    # Address fields
    village_or_town = Column(String, nullable=True)
    landmark = Column(String, nullable=True)
    house_number = Column(String, nullable=True)
    district = Column(String, nullable=True)
    state = Column(String, nullable=True)
    country = Column(String, nullable=True)

    kyc_status = Column(String, default="Pending")
    fatca_status = Column(String, default="Pending")
    nomination_status = Column(String, default="Not Added")

    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
