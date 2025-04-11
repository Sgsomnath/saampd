# app/admin/dashboard_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime, timedelta

from app.core.database.session import get_db
from app.core.models.distributor import Distributor
from app.core.models.investor import Investor
from app.core.models.commission import Commission
from jwt_auth.dependencies import verify_token
from app.admin.auth_dependency import verify_admin_access

router = APIRouter(prefix="/admin/dashboard", tags=["Admin Dashboard"])

# ✅ 1. Summary with totals
@router.get("/summary")
def dashboard_summary(
    db: Session = Depends(get_db),
    current_admin: dict = Depends(verify_token)
):
    verify_admin_access(current_admin)

    total_distributors = db.query(Distributor).count()
    total_investors = db.query(Investor).count()
    total_commission = db.query(func.sum(Commission.amount)).scalar() or 0.0

    return {
        "total_distributors": total_distributors,
        "total_investors": total_investors,
        "total_commission_paid": float(total_commission)
    }

# ✅ 2. Bar chart: Distributor vs Investor count
@router.get("/chart/distributor-vs-investor")
def dashboard_bar_chart(
    db: Session = Depends(get_db),
    current_admin: dict = Depends(verify_token)
):
    verify_admin_access(current_admin)

    distributor_count = db.query(Distributor).count()
    investor_count = db.query(Investor).count()

    return {
        "labels": ["Distributors", "Investors"],
        "data": [distributor_count, investor_count]
    }

# ✅ 3. Line chart: Growth in last 6 months
@router.get("/chart/monthly-growth")
def dashboard_growth_chart(
    db: Session = Depends(get_db),
    current_admin: dict = Depends(verify_token)
):
    verify_admin_access(current_admin)

    today = datetime.today()
    six_months_ago = today - timedelta(days=180)

    dist_data = (
        db.query(
            extract("month", Distributor.created_at).label("month"),
            func.count(Distributor.id).label("count")
        )
        .filter(Distributor.created_at >= six_months_ago)
        .group_by("month")
        .order_by("month")
        .all()
    )

    inv_data = (
        db.query(
            extract("month", Investor.created_at).label("month"),
            func.count(Investor.id).label("count")
        )
        .filter(Investor.created_at >= six_months_ago)
        .group_by("month")
        .order_by("month")
        .all()
    )

    month_map = {
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
        7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
    }

    return {
        "labels": [month_map[int(row.month)] for row in dist_data],
        "distributor_counts": [row.count for row in dist_data],
        "investor_counts": [row.count for row in inv_data],
    }

# ✅ 4. Latest Registered Users
@router.get("/recent-users")
def dashboard_recent_users(
    db: Session = Depends(get_db),
    current_admin: dict = Depends(verify_token)
):
    verify_admin_access(current_admin)

    recent_distributors = db.query(Distributor).order_by(Distributor.created_at.desc()).limit(5).all()
    recent_investors = db.query(Investor).order_by(Investor.created_at.desc()).limit(5).all()

    return {
        "recent_distributors": [
            {"id": d.id, "name": d.name, "email": d.email, "created_at": d.created_at}
            for d in recent_distributors
        ],
        "recent_investors": [
            {"id": i.id, "name": i.name, "email": i.email, "created_at": i.created_at}
            for i in recent_investors
        ]
    }
