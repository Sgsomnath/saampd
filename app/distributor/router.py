from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from app.core.database.dependency import get_db
from app.core.models.distributor import Distributor
from jwt_auth.password_handler import get_password_hash, verify_password
from jwt_auth.token_handler import create_access_token
from typing import Optional
from datetime import date

router = APIRouter(prefix="/distributor", tags=["Distributor"])

# 🔹 Schemas
class DistributorCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    arn_code: str
    phone_number: str
    date_of_birth: Optional[date]
    gender: Optional[str]
    pan_number: Optional[str]
    aadhar_number: Optional[str]
    village_or_town: Optional[str]
    landmark: Optional[str]
    house_number: Optional[str]
    district: Optional[str]
    state: Optional[str]
    country: Optional[str]

class DistributorLogin(BaseModel):
    email: EmailStr
    password: str

class DistributorResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    arn_code: str

    class Config:
        from_attributes = True

class DistributorLoginResponse(BaseModel):
    access_token: str
    token_type: str

# 🔹 Routes
@router.get("/")
def distributor_home():
    return {"message": "Welcome to the Distributor API"}

# ✅ Register Distributor
@router.post("/register", response_model=DistributorResponse)
def register_distributor(distributor: DistributorCreate, db: Session = Depends(get_db)):
    existing_email = db.query(Distributor).filter(Distributor.email == distributor.email).first()
    existing_arn = db.query(Distributor).filter(Distributor.arn_code == distributor.arn_code).first()

    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered.")
    if existing_arn:
        raise HTTPException(status_code=400, detail="ARN code already in use.")

    hashed_pwd = get_password_hash(distributor.password)

    new_distributor = Distributor(
        name=distributor.name,
        email=distributor.email,
        hashed_password=hashed_pwd,
        arn_code=distributor.arn_code,
        phone_number=distributor.phone_number,
        date_of_birth=str(distributor.date_of_birth) if distributor.date_of_birth else None,
        gender=distributor.gender,
        pan_number=distributor.pan_number,
        aadhar_number=distributor.aadhar_number,
        village_or_town=distributor.village_or_town,
        landmark=distributor.landmark,
        house_number=distributor.house_number,
        district=distributor.district,
        state=distributor.state,
        country=distributor.country,
    )
    db.add(new_distributor)
    db.commit()
    db.refresh(new_distributor)
    return new_distributor

# ✅ Login Distributor
@router.post("/login", response_model=DistributorLoginResponse)
def login_distributor(distributor: DistributorLogin, db: Session = Depends(get_db)):
    db_distributor = db.query(Distributor).filter(Distributor.email == distributor.email).first()
    if not db_distributor:
        raise HTTPException(status_code=401, detail="Invalid email")

    if not verify_password(distributor.password, db_distributor.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    token = create_access_token(data={"sub": str(db_distributor.id), "role": "distributor"})
    return {
        "access_token": token,
        "token_type": "bearer"
    }
