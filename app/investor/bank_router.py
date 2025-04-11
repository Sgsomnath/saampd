from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database.session import get_db
from jwt_auth.dependencies import verify_token

router = APIRouter(prefix="/investor/bank", tags=["Investor Bank"])

linked_banks = {}  # mock storage

@router.post("/add")
def add_bank(account_number: str, ifsc: str, upi_id: str, current_investor: dict = Depends(verify_token)):
    linked_banks[current_investor["sub"]] = {
        "account_number": account_number,
        "ifsc": ifsc,
        "upi_id": upi_id
    }
    return {"message": "✅ Bank/UPI info linked successfully"}

@router.get("/")
def get_linked_bank(current_investor: dict = Depends(verify_token)):
    return linked_banks.get(current_investor["sub"], {})
