# app/admin/dashboard_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database.session import get_db
from app.core.models.distributor import Distributor
from app.core.models.investor import Investor
from jwt_auth.dependencies import verify_token  # Admin token verification

router = APIRouter(
    prefix="/admin/dashboard",
    tags=["Admin Dashboard"]
)

# ✅ 1. Summary API: total distributors & investors
@router.get("/summary")
def dashboard_summary(
    db: Session = Depends(get_db),
    current_admin: dict = Depends(verify_token)
):
    total_distributors = db.query(Distributor).count()
    total_investors = db.query(Investor).count()

    return {
        "total_distributors": total_distributors,
        "total_investors": total_investors
    }

# ✅ 2. Chart API: Distributor vs Investor count for bar chart
@router.get("/chart/distributor-vs-investor")
def dashboard_chart(
    db: Session = Depends(get_db),
    current_admin: dict = Depends(verify_token)
):
    distributor_count = db.query(Distributor).count()
    investor_count = db.query(Investor).count()

    return {
        "labels": ["Distributors", "Investors"],
        "data": [distributor_count, investor_count]
    }
