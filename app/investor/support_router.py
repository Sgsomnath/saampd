from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database.session import get_db
from jwt_auth.dependencies import verify_token

router = APIRouter(prefix="/investor/support", tags=["Investor Support"])

@router.post("/feedback")
def submit_feedback(message: str, db: Session = Depends(get_db), current_investor: dict = Depends(verify_token)):
    # Store or send email (you can extend later)
    print(f"Support message from investor ID {current_investor['sub']}: {message}")
    return {"message": "✅ Feedback received. We’ll contact you shortly."}
