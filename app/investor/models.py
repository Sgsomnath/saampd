from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database.session import Base


class Investor(Base):
    __tablename__ = "investors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    mobile = Column(String(15), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String(10), nullable=True)

    pan_number = Column(String(20), nullable=True)
    aadhar_number = Column(String(20), nullable=True)

    # Address
    village_or_town = Column(String(100), nullable=True)
    landmark = Column(String(100), nullable=True)
    house_number = Column(String(50), nullable=True)
    district = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)

    # Extra statuses
    kyc_status = Column(String(50), nullable=True)
    fatca_status = Column(String(50), nullable=True)
    nomination_status = Column(String(50), nullable=True)

    # Meta
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)