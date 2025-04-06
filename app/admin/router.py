from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import auth, utils, database
from app.admin import schemas, models

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

# ✅ Admin registration route
@router.post("/register", response_model=schemas.AdminResponse)
def register_admin(admin: schemas.AdminCreate, db: Session = Depends(database.get_db)):
    existing_admin = db.query(models.Admin).filter(models.Admin.email == admin.email).first()
    if existing_admin:
        raise HTTPException(status_code=400, detail="Admin with this email already exists.")
    
    hashed_password = utils.get_password_hash(admin.password)
    new_admin = models.Admin(name=admin.name, email=admin.email, password=hashed_password)
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin

# ✅ Admin login route
@router.post("/login")
def login_admin(admin: schemas.AdminLogin, db: Session = Depends(database.get_db)):
    db_admin = db.query(models.Admin).filter(models.Admin.email == admin.email).first()
    if not db_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not utils.verify_password(admin.password, db_admin.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = auth.create_access_token(data={"sub": db_admin.email, "role": "admin"})
    return {"access_token": access_token, "token_type": "bearer"}
