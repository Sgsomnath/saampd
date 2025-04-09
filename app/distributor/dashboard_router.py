# app/distributor/dashboard_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database.session import get_db
from app.core.models import Investor  # Assuming Investor model has distributor_id, risk_profile, etc.
from jwt_auth.dependencies import verify_token

router = APIRouter(
    prefix="/distributor/dashboard",
    tags=["Distributor Dashboard"]
)

# ✅ Summary Dashboard for Distributor
@router.get("/summary")
def distributor_dashboard_summary(
    db: Session = Depends(get_db),
    current_distributor: dict = Depends(verify_token)
):
    distributor_id = int(current_distributor["sub"])

    total_investors = db.query(Investor).filter(Investor.distributor_id == distributor_id).count()

    # Mock values for investment summary
    total_investment = 750000  # Example static value
    sip_count = 10
    stp_count = 2
    swp_count = 1

    # Mock login summary
    logins_today = 3
    logins_week = 15

    # Pie chart distribution of risk profile
    risk_distribution = db.query(Investor.risk_profile).filter(
        Investor.distributor_id == distributor_id
    ).all()
    profile_count = {"Low": 0, "Medium": 0, "High": 0}
    for risk in risk_distribution:
        profile_count[risk[0]] += 1

    return {
        "total_investors": total_investors,
        "total_investment": total_investment,
        "sip_count": sip_count,
        "stp_count": stp_count,
        "swp_count": swp_count,
        "logins_today": logins_today,
        "logins_week": logins_week,
        "risk_pie_chart": {
            "labels": ["Low", "Medium", "High"],
            "data": [
                profile_count["Low"],
                profile_count["Medium"],
                profile_count["High"]
            ]
        }
    }
