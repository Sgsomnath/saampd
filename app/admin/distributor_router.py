from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database.session import get_db
from app.core.models.distributor import Distributor
from jwt_auth.dependencies import verify_token
from app.admin.auth_dependency import verify_admin_access  # 🔐 Admin-only access

router = APIRouter(prefix="/admin/distributors", tags=["Admin - Distributors"])

# 🔹 Get all distributors
@router.get("/")
def get_all_distributors(
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    verify_admin_access(current_user)

    distributors = db.query(Distributor).all()
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

# 🔹 View single distributor by ID
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
        "created_at": distributor.created_at
    }

# 🔹 Search distributors
@router.get("/search")
def search_distributors(
    keyword: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    verify_admin_access(current_user)

    results = db.query(Distributor).filter(
        (Distributor.name.ilike(f"%{keyword}%")) |
        (Distributor.email.ilike(f"%{keyword}%")) |
        (Distributor.mobile.ilike(f"%{keyword}%"))
    ).all()

    return [
        {
            "id": d.id,
            "name": d.name,
            "email": d.email,
            "mobile": d.mobile,
            "is_active": d.is_active,
            "created_at": d.created_at
        }
        for d in results
    ]

# 🔹 Block / Unblock Distributor
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
