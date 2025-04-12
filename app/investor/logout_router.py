# app/investor/logout_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database.session import get_db
from jwt_auth.dependencies import verify_token

router = APIRouter(
    prefix="/investor/dashboard",
    tags=["Investor Dashboard"]
)

# ✅ Logout All Devices (Mock version) with custom operation_id
@router.post("/logout", operation_id="logout_all_devices_investor_dashboard")
def logout_all_devices(
    db: Session = Depends(get_db),
    current_investor: dict = Depends(verify_token)
):
    # 🔒 Normally: Store revoked tokens or invalidate them from cache
    return {"message": "✅ Logged out from all devices"}
