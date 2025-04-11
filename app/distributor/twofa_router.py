from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from sqlalchemy.orm import Session
import random

from app.core.database.session import get_db
from jwt_auth.dependencies import verify_token
from app.core.models.distributor import Distributor
from app.core.config.settings import settings

router = APIRouter(prefix="/distributor/2fa", tags=["Distributor 2FA"])

# ✅ Email Configuration (fully compatible with FastAPI-Mail)
conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_STARTTLS=settings.mail_starttls,
    MAIL_SSL_TLS=settings.mail_ssl_tls,
    USE_CREDENTIALS=True
)

# ✅ In-memory store for OTPs
otp_store = {}

@router.get("/send-otp")
def send_otp(
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    distributor = db.query(Distributor).filter(Distributor.id == int(current_user["sub"])).first()
    if not distributor:
        raise HTTPException(status_code=404, detail="Distributor not found")

    otp = str(random.randint(100000, 999999))
    otp_store[distributor.email] = otp

    message = MessageSchema(
        subject="Your OTP for Verification",
        recipients=[distributor.email],
        body=f"Dear {distributor.name},\n\nYour OTP is: {otp}\n\nThank you.",
        subtype="plain"
    )

    fm = FastMail(conf)
    fm.send_message(message)
    return {"message": f"📧 OTP sent to {distributor.email}"}

@router.post("/verify-otp")
def verify_otp(
    otp: str = Query(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    distributor = db.query(Distributor).filter(Distributor.id == int(current_user["sub"])).first()
    if not distributor:
        raise HTTPException(status_code=404, detail="Distributor not found")

    if otp_store.get(distributor.email) == otp:
        del otp_store[distributor.email]
        return {"message": "✅ OTP verified successfully"}
    else:
        raise HTTPException(status_code=400, detail="❌ Invalid OTP")

@router.put("/change-email")
def change_email_with_otp(
    new_email: EmailStr = Query(...),
    otp: str = Query(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    distributor = db.query(Distributor).filter(Distributor.id == int(current_user["sub"])).first()
    if not distributor:
        raise HTTPException(status_code=404, detail="Distributor not found")

    if otp_store.get(distributor.email) != otp:
        raise HTTPException(status_code=400, detail="❌ Invalid OTP")

    if db.query(Distributor).filter(Distributor.email == new_email).first():
        raise HTTPException(status_code=400, detail="❌ Email already in use")

    distributor.email = new_email
    db.commit()
    del otp_store[distributor.email]
    return {"message": "📧 Email updated successfully!"}
