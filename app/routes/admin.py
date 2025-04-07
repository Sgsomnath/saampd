from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import auth, utils
from app.database import get_db
from app.admin.models import Admin
from app.admin.schemas import AdminCreate, AdminResponse, AdminLogin

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/")
def admin_home():
    return {"message": "Welcome to the Admin API"}

@router.post("/register", response_model=AdminResponse)
def register_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    try:
        # Check if the admin already exists
        existing_admin = db.query(Admin).filter(Admin.email == admin.email).first()
        if existing_admin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Admin with this email already exists."
            )

        # Hash the password and create a new admin
        hashed_password = utils.get_password_hash(admin.password)
        new_admin = Admin(name=admin.name, email=admin.email, password=hashed_password)
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        return new_admin

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error registering admin: {e}"
        )

@router.post("/login")
def login_admin(admin: AdminLogin, db: Session = Depends(get_db)):
    db_admin = db.query(Admin).filter(Admin.email == admin.email).first()
    if not db_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    
    if not utils.verify_password(admin.password, db_admin.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

    token = auth.create_access_token(data={"sub": db_admin.email})
    return {
        "access_token": token,
        "token_type": "bearer"
    }
