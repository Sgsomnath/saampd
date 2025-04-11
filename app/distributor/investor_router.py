# app/distributor/investor_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database.session import get_db
from app.core.models.investor import Investor
from jwt_auth.dependencies import verify_token
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/distributor/investors", tags=["Distributor Investors"])

class InvestorSummary(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True

# ✅ Get all investors (Mock: linked to this distributor)
@router.get("/", response_model=list[InvestorSummary])
def get_investors(
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    return db.query(Investor).all()

# ✅ Add investor manually (Mock)
@router.post("/add")
def add_investor(
    investor: InvestorSummary,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    exists = db.query(Investor).filter(Investor.email == investor.email).first()
    if exists:
        raise HTTPException(status_code=400, detail="Investor already exists.")
    
    new_investor = Investor(
        name=investor.name,
        email=investor.email,
        is_active=investor.is_active
    )
    db.add(new_investor)
    db.commit()
    db.refresh(new_investor)
    return {"message": "✅ Investor added manually"}
