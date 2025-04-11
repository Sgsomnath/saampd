from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.core.database.session import get_db
from jwt_auth.dependencies import verify_token
from app.core.models.investor import Investor
from jwt_auth.password_handler import verify_password, get_password_hash
from app.investor.schemas import (
    InvestorProfile,
    InvestorProfileUpdate,
    ChangePasswordRequest,
    KYCStatusUpdate,
    NomineeUpdate
)
import os
import shutil

router = APIRouter(
    prefix="/investor/profile",
    tags=["Investor Profile"]
)

# ✅ GET profile
@router.get("/", response_model=InvestorProfile)
def get_profile(
    db: Session = Depends(get_db),
    current_investor: dict = Depends(verify_token)
):
    investor_id = int(current_investor["sub"])
    investor = db.query(Investor).filter(Investor.id == investor_id).first()
    if not investor:
        raise HTTPException(status_code=404, detail="Investor not found")
    return investor


# ✅ UPDATE profile
@router.put("/", response_model=InvestorProfile)
def update_profile(
    update_data: InvestorProfileUpdate,
    db: Session = Depends(get_db),
    current_investor: dict = Depends(verify_token)
):
    investor_id = int(current_investor["sub"])
    investor = db.query(Investor).filter(Investor.id == investor_id).first()
    if not investor:
        raise HTTPException(status_code=404, detail="Investor not found")

    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(investor, field, value)

    db.commit()
    db.refresh(investor)
    return investor


# ✅ CHANGE Password
@router.put("/change-password")
def change_password(
    req: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_investor: dict = Depends(verify_token)
):
    investor_id = int(current_investor["sub"])
    investor = db.query(Investor).filter(Investor.id == investor_id).first()
    if not investor:
        raise HTTPException(status_code=404, detail="Investor not found")

    if not verify_password(req.old_password, investor.hashed_password):
        raise HTTPException(status_code=401, detail="Old password is incorrect")

    investor.hashed_password = get_password_hash(req.new_password)
    db.commit()
    return {"message": "✅ Password changed successfully"}


# ✅ UPDATE KYC/FATCA Status
@router.put("/kyc-fatca")
def update_kyc_fatca(
    req: KYCStatusUpdate,
    db: Session = Depends(get_db),
    current_investor: dict = Depends(verify_token)
):
    investor_id = int(current_investor["sub"])
    investor = db.query(Investor).filter(Investor.id == investor_id).first()

    if not investor:
        raise HTTPException(status_code=404, detail="Investor not found")

    if req.kyc_status:
        investor.kyc_status = req.kyc_status
    if req.fatca_status:
        investor.fatca_status = req.fatca_status

    db.commit()
    return {"message": "✅ KYC/FATCA status updated"}


# ✅ UPDATE Nominee Info
@router.put("/nominee")
def update_nominee(
    req: NomineeUpdate,
    db: Session = Depends(get_db),
    current_investor: dict = Depends(verify_token)
):
    investor_id = int(current_investor["sub"])
    investor = db.query(Investor).filter(Investor.id == investor_id).first()

    if not investor:
        raise HTTPException(status_code=404, detail="Investor not found")

    investor.nomination_status = req.nomination_status
    db.commit()
    return {"message": "✅ Nominee information updated"}


# ✅ UPLOAD Avatar/Profile Picture
@router.put("/avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_investor: dict = Depends(verify_token)
):
    investor_id = int(current_investor["sub"])
    folder = "uploads/avatars"
    os.makedirs(folder, exist_ok=True)

    ext = file.filename.split(".")[-1].lower()
    if ext not in ["jpg", "jpeg", "png"]:
        raise HTTPException(status_code=400, detail="Only JPG or PNG allowed")

    filename = f"investor_{investor_id}.{ext}"
    file_path = os.path.join(folder, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": "✅ Avatar uploaded successfully", "file": filename}


# ✅ Email Verification (Mock)
@router.get("/verify-email")
def verify_email(code: str = Query(..., description="Enter the 6-digit verification code")):
    if code == "123456":
        return {"message": "✅ Email verified successfully"}
    else:
        raise HTTPException(status_code=400, detail="Invalid verification code")


# ✅ Logout All Devices (Mock JWT Revoke)
@router.post("/logout")
def logout_all_devices(
    current_investor: dict = Depends(verify_token)
):
    # In production: track tokens & mark them invalid
    return {"message": "✅ Logged out from all devices"}
