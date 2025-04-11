from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database.session import get_db
from app.core.models.distributor import Distributor
from jwt_auth.dependencies import verify_token
from app.admin.auth_dependency import verify_admin_access  # 🔐 Admin-only access

router = APIRouter(prefix="/admin/distributors", tags=["Admin - Distributors"])

# 🔍 Get all or search distributors
@router.get("/")
def get_all_distributors(
    keyword: str = Query(None),
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    verify_admin_access(current_user)

    query = db.query(Distributor)
    if keyword:
        keyword = f"%{keyword.lower()}%"
        query = query.filter(
            Distributor.name.ilike(keyword) |
            Distributor.email.ilike(keyword) |
            Distributor.mobile.ilike(keyword)
        )

    distributors = query.order_by(Distributor.created_at.desc()).all()

    return [
        {
            "id": d.id,
            "name": d.name,
            "email": d.email,
            "mobile": d.mobile,
            "is_active": d.is_active,
            "created_at": d.created_at
        }
        for d in distributors
    ]

# 👁️ View full details of a distributor
@router.get("/view/{distributor_id}")
def view_distributor(
    distributor_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    verify_admin_access(current_user)

    distributor = db.query(Distributor).filter(Distributor.id == distributor_id).first()
    if not distributor:
        raise HTTPException(status_code=404, detail="Distributor not found")

    return {
        "id": distributor.id,
        "name": distributor.name,
        "email": distributor.email,
        "mobile": distributor.mobile,
        "is_active": distributor.is_active,
        "created_at": distributor.created_at,
        "avatar_url": distributor.avatar_url,
        "payout_details": distributor.payout_details,
        "last_login": distributor.last_login
    }

# 🔒 Block / Unblock distributor
@router.put("/toggle-status/{distributor_id}")
def toggle_distributor_status(
    distributor_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    verify_admin_access(current_user)

    distributor = db.query(Distributor).filter(Distributor.id == distributor_id).first()
    if not distributor:
        raise HTTPException(status_code=404, detail="Distributor not found")

    distributor.is_active = not distributor.is_active
    db.commit()

    status = "unblocked" if distributor.is_active else "blocked"
    return {"message": f"Distributor has been {status} successfully."}
