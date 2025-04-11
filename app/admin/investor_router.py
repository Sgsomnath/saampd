# app/admin/investor_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database.session import get_db
from app.core.models.investor import Investor
from jwt_auth.dependencies import verify_token

router = APIRouter(prefix="/admin/investors", tags=["Admin Investor View"])

@router.get("/")
def get_all_investors(db: Session = Depends(get_db), current_user: dict = Depends(verify_token)):
    investors = db.query(Investor).all()
    if not investors:
        raise HTTPException(status_code=404, detail="No investors found")

    return [{"id": inv.id, "name": inv.name, "email": inv.email, "mobile": inv.mobile} for inv in investors]
