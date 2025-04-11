# app/investor/router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database.dependency import get_db
from app.core.models.investor import Investor

# 🔹 Schemas
from app.investor.schemas import (
    InvestorCreate,
    InvestorLogin,
    InvestorResponse,
    InvestorLoginResponse,
)

# 🔐 Auth tools
from jwt_auth.password_handler import get_password_hash, verify_password
from jwt_auth.token_handler import create_access_token

router = APIRouter(
    prefix="/investor",
    tags=["Investor"]
)

# ✅ Investor Home
@router.get("/")
def investor_home():
    return {"message": "Welcome to the Investor API"}


# ✅ Register Investor
@router.post("/register", response_model=InvestorResponse)
def register_investor(
    investor: InvestorCreate,
    db: Session = Depends(get_db)
):
    # 🔐 Email, mobile & PAN must be unique
    if db.query(Investor).filter(Investor.email == investor.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    if db.query(Investor).filter(Investor.mobile == investor.mobile).first():
        raise HTTPException(status_code=400, detail="Mobile number already in use")
    if db.query(Investor).filter(Investor.pan == investor.pan).first():
        raise HTTPException(status_code=400, detail="PAN already exists")

    hashed_password = get_password_hash(investor.password)

    new_investor = Investor(
        name=investor.name,
        email=investor.email,
        password=investor.password,
        hashed_password=hashed_password,
        mobile=investor.mobile,
        dob=investor.dob,
        gender=investor.gender,
        pan=investor.pan,
        aadhar=investor.aadhar,
        address=investor.address
    )
    db.add(new_investor)
    db.commit()
    db.refresh(new_investor)
    return new_investor


# ✅ Login Investor
@router.post("/login", response_model=InvestorLoginResponse)
def login_investor(
    investor: InvestorLogin,
    db: Session = Depends(get_db)
):
    db_investor = db.query(Investor).filter(Investor.email == investor.email).first()
    if not db_investor:
        raise HTTPException(status_code=401, detail="Invalid email")

    if not verify_password(investor.password, db_investor.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    token = create_access_token(data={"sub": str(db_investor.id), "role": "investor"})

    return {
        "access_token": token,
        "token_type": "bearer"
    }
