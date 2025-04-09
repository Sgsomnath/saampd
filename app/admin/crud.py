# app/admin/crud.py

from sqlalchemy.orm import Session
from app.admin import schemas, models
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_admin(db: Session, admin: schemas.AdminCreate):
    hashed_password = get_password_hash(admin.password)
    db_admin = models.Admin(
        name=admin.name,
        email=admin.email,
        hashed_password=hashed_password
    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

def get_admin_by_email(db: Session, email: str):
    return db.query(models.Admin).filter(models.Admin.email == email).first()

def get_admins(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Admin).offset(skip).limit(limit).all()

