from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database.session import get_db
from app.core.models.distributor import Distributor
from jwt_auth.dependencies import verify_token
from app.admin.auth_dependency import verify_admin_access  # 🔐 Admin-only access

router = APIRouter(prefix="/admin/distributors", tags=["Admin - Distributors"])

@router.get("/")
def get_all_distributors(
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    verify_admin_access(current_user)  # 🛡️ Ensure only admin can access

    distributors = db.query(Distributor).all()
    return [  # 🧾 Cleaned-up response
        {
            "id": d.id,
            "name": d.name,
            "email": d.email,
            "mobile": d.mobile,
            "created_at": d.created_at
        }
        for d in distributors
    ]
