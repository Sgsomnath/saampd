from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database.session import get_db
from app.core.models.investor import Investor
from jwt_auth.dependencies import verify_token
from app.admin.auth_dependency import verify_admin_access  # 🛡️ Admin-only

router = APIRouter(prefix="/admin/investors", tags=["Admin - Investors"])

# 🔍 Get all / Search Investors
@router.get("/")
def get_all_investors(
    keyword: str = Query(None),
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    verify_admin_access(current_user)

    query = db.query(Investor)
    if keyword:
        keyword = f"%{keyword.lower()}%"
        query = query.filter(
            Investor.name.ilike(keyword) |
            Investor.email.ilike(keyword) |
            Investor.mobile.ilike(keyword)
        )

    investors = query.order_by(Investor.created_at.desc()).all()

    return [
        {
            "id": i.id,
            "name": i.name,
            "email": i.email,
            "mobile": i.mobile,
            "is_active": i.is_active,
            "created_at": i.created_at
        }
        for i in investors
    ]

# 👁️ Get single investor
@router.get("/view/{investor_id}")
def get_single_investor(
    investor_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    verify_admin_access(current_user)

    investor = db.query(Investor).filter(Investor.id == investor_id).first()
    if not investor:
        raise HTTPException(status_code=404, detail="Investor not found")

    return {
        "id": investor.id,
        "name": investor.name,
        "email": investor.email,
        "mobile": investor.mobile,
        "is_active": investor.is_active,
        "created_at": investor.created_at
    }

# 🔒 Block investor
@router.put("/block/{investor_id}")
def block_investor(
    investor_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    verify_admin_access(current_user)

    investor = db.query(Investor).filter(Investor.id == investor_id).first()
    if not investor:
        raise HTTPException(status_code=404, detail="Investor not found")

    investor.is_active = False
    db.commit()
    return {"message": "🚫 Investor blocked"}

# ✅ Unblock investor
@router.put("/unblock/{investor_id}")
def unblock_investor(
    investor_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    verify_admin_access(current_user)

    investor = db.query(Investor).filter(Investor.id == investor_id).first()
    if not investor:
        raise HTTPException(status_code=404, detail="Investor not found")

    investor.is_active = True
    db.commit()
    return {"message": "✅ Investor unblocked"}

# 🗑️ Delete investor
@router.delete("/delete/{investor_id}")
def delete_investor(
    investor_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    verify_admin_access(current_user)

    investor = db.query(Investor).filter(Investor.id == investor_id).first()
    if not investor:
        raise HTTPException(status_code=404, detail="Investor not found")

    db.delete(investor)
    db.commit()
    return {"message": "🗑️ Investor deleted successfully"}
