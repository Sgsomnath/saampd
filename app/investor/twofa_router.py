from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from sqlalchemy.orm import Session
import random

from app.core.database.session import get_db
from jwt_auth.dependencies import verify_token
from app.core.models.investor import Investor
from app.core.config.settings import settings

router = APIRouter(prefix="/investor/2fa", tags=["Investor 2FA"])

# ✅ Email config (clean and correct)
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

# ✅ OTP Store (temporary, in-memory)
otp_store = {}

# ✅ Send OTP
@router.get("/send-otp")
def send_otp(
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    investor = db.query(Investor).filter(Investor.id == int(current_user["sub"])).first()
    if not investor:
        raise HTTPException(status_code=404, detail="Investor not found")

    otp = str(random.randint(100000, 999999))
    otp_store[investor.email] = otp

    message = MessageSchema(
        subject="Your OTP for Verification",
        recipients=[investor.email],
        body=f"Your OTP is: {otp}",
        subtype="plain"
    )

    fm = FastMail(conf)
    fm.send_message(message)
    return {"message": f"📧 OTP sent to {investor.email}"}

# ✅ Verify OTP
@router.post("/verify-otp")
def verify_otp(
    otp: str = Query(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    investor = db.query(Investor).filter(Investor.id == int(current_user["sub"])).first()
    if not investor:
        raise HTTPException(status_code=404, detail="Investor not found")

    if otp_store.get(investor.email) == otp:
        del otp_store[investor.email]
        return {"message": "✅ OTP verified successfully"}
    else:
        raise HTTPException(status_code=400, detail="❌ Invalid OTP")

# ✅ Change Email with OTP
@router.put("/change-email")
def change_email_with_otp(
    new_email: EmailStr = Query(...),
    otp: str = Query(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    investor = db.query(Investor).filter(Investor.id == int(current_user["sub"])).first()
    if not investor:
        raise HTTPException(status_code=404, detail="Investor not found")

    if otp_store.get(investor.email) != otp:
        raise HTTPException(status_code=400, detail="❌ Invalid OTP")

    if db.query(Investor).filter(Investor.email == new_email).first():
        raise HTTPException(status_code=400, detail="❌ Email already in use")

    investor.email = new_email
    db.commit()
    del otp_store[investor.email]
    return {"message": "📧 Email updated successfully!"}
