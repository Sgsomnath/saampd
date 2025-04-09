# app/admin/routes.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# ✅ JWT/Auth import (from root-level jwt_auth/)
from jwt_auth.token_handler import create_access_token
from jwt_auth.password_handler import get_password_hash, verify_password
from jwt_auth.dependencies import verify_token

# ✅ Database & Admin schema/model
from app.core.database.session import get_db
from app.admin.models import Admin
from app.admin.schemas import AdminCreate, AdminResponse, AdminLogin, AdminLoginResponse

router = APIRouter(prefix="/admin", tags=["Admin"])


# ✅ Admin Home (Protected Route)
@router.get("/", response_model=dict)
def admin_home(current_admin: Admin = Depends(verify_token)):
    return {"message": f"Welcome, {current_admin.name}!"}


# ✅ Register Admin
@router.post("/register", response_model=AdminResponse)
def register_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    existing_admin = db.query(Admin).filter(Admin.email == admin.email).first()
    if existing_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin with this email already exists."
        )

    hashed_password = get_password_hash(admin.password)
    new_admin = Admin(name=admin.name, email=admin.email, password=hashed_password)
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin


# ✅ Login Admin
@router.post("/login", response_model=AdminLoginResponse)
def login_admin(admin: AdminLogin, db: Session = Depends(get_db)):
    db_admin = db.query(Admin).filter(Admin.email == admin.email).first()
    if not db_admin or not verify_password(admin.password, db_admin.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token_data = {"sub": str(db_admin.id), "role": "admin"}
    access_token = create_access_token(data=token_data)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
