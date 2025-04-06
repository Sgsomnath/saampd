from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import utils, auth
from app.database import get_db
from app.admin.models import Admin
from app.admin import schemas

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/")
def admin_home():
    return {"message": "Welcome to the Admin API"}

@router.post("/register")
def register_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    db_admin = db.query(Admin).filter(Admin.email == admin.email).first()
    if db_admin:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = utils.hash_password(admin.password)
    new_admin = Admin(email=admin.email, password=hashed_password)
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return {"message": "Admin registered successfully"}

@router.post("/login")
def login_admin(admin: schemas.AdminLogin, db: Session = Depends(get_db)):
    db_admin = db.query(Admin).filter(Admin.email == admin.email).first()
    if not db_admin:
        raise HTTPException(status_code=401, detail="Invalid email")
    
    if not utils.verify_password(admin.password, db_admin.password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    token = auth.create_access_token(data={"sub": db_admin.email})
    return {
        "access_token": token,
        "token_type": "bearer"
    }
