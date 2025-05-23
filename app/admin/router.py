from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from jwt_auth.token_handler import create_access_token
from jwt_auth.password_handler import get_password_hash, verify_password
from jwt_auth.dependencies import verify_token

from app.core.database.session import get_db
from app.core.models.admin import Admin
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
    new_admin = Admin(
        name=admin.name,
        email=admin.email,
        hashed_password=hashed_password,
        phone_number=admin.mobile
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return AdminResponse(
        id=new_admin.id,
        name=new_admin.name,
        email=new_admin.email,
        mobile=new_admin.phone_number
    )


# ✅ Login Admin
@router.post("/login", response_model=AdminLoginResponse)
def login_admin(admin: AdminLogin, db: Session = Depends(get_db)):
    db_admin = db.query(Admin).filter(Admin.email == admin.email).first()
    if not db_admin or not verify_password(admin.password, db_admin.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token_data = {"sub": str(db_admin.id), "role": "admin"}
    access_token = create_access_token(data=token_data)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }