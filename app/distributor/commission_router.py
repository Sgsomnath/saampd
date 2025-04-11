# app/distributor/commission_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database.session import get_db
from jwt_auth.dependencies import verify_token

router = APIRouter(prefix="/distributor/commission", tags=["Commission"])

@router.get("/summary")
def get_commission_summary(
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    return {
        "total_commission": "₹15,200",
        "this_month": "₹2,300",
        "last_month": "₹1,980"
    }

@router.get("/breakdown")
def get_commission_breakdown(
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    return [
        {"scheme": "HDFC Balanced Fund", "amount": 500},
        {"scheme": "SBI Equity Fund", "amount": 400},
        {"scheme": "ICICI Value Discovery", "amount": 600},
    ]
