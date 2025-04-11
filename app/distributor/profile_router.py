# app/distributor/profile_router.py

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.core.database.session import get_db
from jwt_auth.dependencies import verify_token
from app.core.models.distributor import Distributor
from jwt_auth.password_handler import verify_password, get_password_hash
import shutil, os, uuid
from pydantic import BaseModel, EmailStr

router = APIRouter(
    prefix="/distributor/profile",
    tags=["Distributor Profile"]
)

# ⛓️ SCHEMAS
class DistributorProfile(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str | None = None
    company: str | None = None
    avatar: str | None = None

    class Config:
        from_attributes = True

class DistributorProfileUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    company: str | None = None

class DistributorChangePassword(BaseModel):
    old_password: str
    new_password: str

# ✅ GET Profile
@router.get("/", response_model=DistributorProfile)
def get_profile(
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    distributor = db.query(Distributor).filter(Distributor.id == int(current_user["sub"])).first()
    if not distributor:
        raise HTTPException(status_code=404, detail="Distributor not found")
    return distributor

# ✅ UPDATE Profile
@router.put("/", response_model=DistributorProfile)
def update_profile(
    update: DistributorProfileUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    distributor = db.query(Distributor).filter(Distributor.id == int(current_user["sub"])).first()
    if not distributor:
        raise HTTPException(status_code=404, detail="Distributor not found")

    for key, value in update.dict(exclude_unset=True).items():
        setattr(distributor, key, value)

    db.commit()
    db.refresh(distributor)
    return distributor

# ✅ CHANGE Password
@router.put("/change-password")
def change_password(
    req: DistributorChangePassword,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    distributor = db.query(Distributor).filter(Distributor.id == int(current_user["sub"])).first()
    if not distributor:
        raise HTTPException(status_code=404, detail="Distributor not found")

    if not verify_password(req.old_password, distributor.hashed_password):
        raise HTTPException(status_code=401, detail="Old password is incorrect")

    distributor.hashed_password = get_password_hash(req.new_password)
    db.commit()
    return {"message": "✅ Password changed successfully"}

# ✅ UPLOAD Avatar
@router.put("/avatar")
def upload_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    distributor_id = int(current_user["sub"])
    folder = f"uploads/distributors/{distributor_id}"
    os.makedirs(folder, exist_ok=True)
    ext = file.filename.split(".")[-1]
    filename = f"avatar_{uuid.uuid4().hex[:8]}.{ext}"
    file_path = os.path.join(folder, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    distributor = db.query(Distributor).filter(Distributor.id == distributor_id).first()
    distributor.avatar = file_path
    db.commit()

    return {"message": "✅ Avatar uploaded", "path": file_path}

# ✅ LOGOUT All Devices
@router.post("/logout")
def logout_all_devices():
    return {"message": "🚪 Logged out from all devices (mock)"}

# ✅ Email Verification (mock)
@router.get("/verify-email")
def verify_email(email: EmailStr = Query(...)):
    return {"message": f"✅ Verification email sent to {email} (mock)"}

# ✅ Device Authorization Log (mock)
@router.get("/devices")
def get_devices():
    return {
        "devices": [
            {"device": "Chrome on Windows", "ip": "103.21.244.1", "last_used": "2024-04-09"},
            {"device": "Mobile App on Android", "ip": "103.99.0.75", "last_used": "2024-04-10"}
        ]
    }

# ✅ Payout Bank Details (mock)
@router.get("/payout-details")
def payout_details():
    return {
        "bank_name": "HDFC Bank",
        "account_number": "XXXXXX1234",
        "ifsc_code": "HDFC0001234",
        "upi_id": "distributor@hdfcbank"
    }
