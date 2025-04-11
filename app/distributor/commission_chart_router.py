from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime, timedelta

from app.core.database.session import get_db
from app.core.models.commission import Commission
from jwt_auth.dependencies import verify_token

router = APIRouter(prefix="/distributor/dashboard/chart", tags=["Distributor Dashboard Chart"])

@router.get("/commission-trend")
def get_commission_trend_chart(
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    # Last 6 months from now
    today = datetime.today()
    six_months_ago = today - timedelta(days=180)

    results = (
        db.query(
            extract('month', Commission.date).label("month"),
            func.sum(Commission.amount).label("total")
        )
        .filter(
            Commission.distributor_id == int(current_user["sub"]),
            Commission.date >= six_months_ago
        )
        .group_by(extract('month', Commission.date))
        .order_by(extract('month', Commission.date))
        .all()
    )

    # Month number to name
    month_names = {
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
        7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
    }

    labels = [month_names[int(row.month)] for row in results]
    values = [float(row.total) for row in results]

    return {"labels": labels, "values": values}
