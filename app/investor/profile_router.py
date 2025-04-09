from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database.session import get_db
from jwt_auth.dependencies import verify_token
from app.core.models.investor import Investor
from app.investor.schemas import InvestorProfile, InvestorResponse, InvestorProfileUpdate
from app.investor.schemas import InvestorProfileUpdate as InvestorUpdate


router = APIRouter(
    prefix="/investor/profile",
    tags=["Investor Profile"]
)

# ✅ GET profile
@router.get("/", response_model=InvestorProfile)
def get_profile(
    db: Session = Depends(get_db),
    current_investor: dict = Depends(verify_token)
):
    investor_id = int(current_investor["sub"])
    investor = db.query(Investor).filter(Investor.id == investor_id).first()
    if not investor:
        raise HTTPException(status_code=404, detail="Investor not found")
    return investor

# ✅ UPDATE profile
@router.put("/", response_model=InvestorProfile)
def update_profile(
    update_data: InvestorProfileUpdate,
    db: Session = Depends(get_db),
    current_investor: dict = Depends(verify_token)
):
    investor_id = int(current_investor["sub"])
    investor = db.query(Investor).filter(Investor.id == investor_id).first()
    if not investor:
        raise HTTPException(status_code=404, detail="Investor not found")

    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(investor, field, value)

    db.commit()
    db.refresh(investor)
    return investor
