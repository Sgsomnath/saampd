from sqlalchemy import Column, Integer, Float, ForeignKey, String, DateTime
from sqlalchemy.sql import func
from app.core.database.base import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    investor_id = Column(Integer, ForeignKey("investors.id"), nullable=False)
    scheme_id = Column(Integer, ForeignKey("schemes.id"), nullable=False)

    transaction_type = Column(String, nullable=False)  # Purchase, SIP, SWP, Redemption, Switch
    amount = Column(Float, nullable=False)
    units = Column(Float, default=0.0)  # Units allotted or redeemed
    nav_at_transaction = Column(Float, default=0.0)  # NAV at time of transaction
    order_id = Column(String, unique=True, index=True)  # BSE Order ID (optional but helpful)
    status = Column(String, default="Pending")  # Pending, Success, Failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Transaction(id={self.id}, investor={self.investor_id}, scheme={self.scheme_id}, type='{self.transaction_type}')>"
