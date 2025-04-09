# app/investor/dashboard_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database.session import get_db
from jwt_auth.dependencies import verify_token

router = APIRouter(
    prefix="/investor/dashboard",
    tags=["Investor Dashboard"]
)

# ✅ 1. Investor Dashboard Summary API (Mock data)
@router.get("/summary")
def investor_dashboard_summary(
    db: Session = Depends(get_db),
    current_investor: dict = Depends(verify_token)
):
    return {
        "total_investment": "₹1,50,000",
        "sip_count": 3,
        "stp_count": 1,
        "lumpsum_count": 2,
        "kyc_status": "Verified",
        "fatca_status": "Pending",
        "nomination_status": "Added"
    }

# ✅ 2. View All Investments (Mock list)
@router.get("/investments")
def investor_investments(
    db: Session = Depends(get_db),
    current_investor: dict = Depends(verify_token)
):
    return [
        {"type": "SIP", "amount": 5000, "date": "2024-05-01"},
        {"type": "Lumpsum", "amount": 100000, "date": "2024-03-15"},
        {"type": "Redemption", "amount": 20000, "date": "2024-06-10"},
    ]

# ✅ 3. Portfolio Pie Chart View (Mock)
@router.get("/portfolio")
def investor_portfolio(
    db: Session = Depends(get_db),
    current_investor: dict = Depends(verify_token)
):
    return {
        "labels": ["Equity", "Debt", "Hybrid"],
        "data": [70, 20, 10]
    }

# ✅ 4. Request Section - New SIP or Redemption
@router.post("/requests")
def create_request(
    request_data: dict,
    db: Session = Depends(get_db),
    current_investor: dict = Depends(verify_token)
):
    # Just storing in mock format for now
    return {
        "status": "success",
        "message": f"Your {request_data.get('type')} request has been recorded."
    }

# ✅ 5. Alerts (KYC/FATCA/Nomination)
@router.get("/alerts")
def investor_alerts(
    db: Session = Depends(get_db),
    current_investor: dict = Depends(verify_token)
):
    return {
        "kyc_alert": False,
        "fatca_alert": True,
        "nomination_alert": False
    }
