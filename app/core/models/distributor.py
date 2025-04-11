from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.core.database.base import Base

class Distributor(Base):
    __tablename__ = "distributors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # 🔹 Identification
    arn_code = Column(String, unique=True, nullable=False)  # ARN (AMFI Registration Number)
    phone_number = Column(String, nullable=False)
    date_of_birth = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    pan_number = Column(String, nullable=True)
    aadhar_number = Column(String, nullable=True)

    # 🔹 Address Info
    village_or_town = Column(String, nullable=True)
    landmark = Column(String, nullable=True)
    house_number = Column(String, nullable=True)
    district = Column(String, nullable=True)
    state = Column(String, nullable=True)
    country = Column(String, nullable=True)

    # 🔹 Optional Fields
    payout_details = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)

    # 🔹 Status & Meta Info
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Distributor(id={self.id}, name='{self.name}', ARN='{self.arn_code}')>"
