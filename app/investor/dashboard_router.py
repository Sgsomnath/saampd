from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.database.session import get_db
from jwt_auth.dependencies import verify_token
import pandas as pd
import os
from typing import Optional

router = APIRouter(
    prefix="/investor/dashboard",
    tags=["Investor Dashboard"]
)

# ✅ 1. Dashboard Summary
@router.get("/summary")
def investor_dashboard_summary(
    db: Session = Depends(get_db),
    current_investor: dict = Depends(verify_token)
):
    return {
        "total_investment": "₹1,50,000",
        "sip_count": 3,
        "stp_count": 1,
        "lumpsum_count": 2,
        "kyc_status": "Verified",
        "fatca_status": "Pending",
        "nomination_status": "Added"
    }


# ✅ 2. All Investments
@router.get("/investments")
def investor_investments(
    db: Session = Depends(get_db),
    current_investor: dict = Depends(verify_token)
):
    return [
        {"type": "SIP", "amount": 5000, "date": "2024-05-01"},
        {"type": "Lumpsum", "amount": 100000, "date": "2024-03-15"},
        {"type": "Redemption", "amount": 20000, "date": "2024-06-10"},
    ]


# ✅ 3. Portfolio Chart
@router.get("/portfolio")
def investor_portfolio(
    db: Session = Depends(get_db),
    current_investor: dict = Depends(verify_token)
):
    return {
        "labels": ["Equity", "Debt", "Hybrid"],
        "data": [70, 20, 10]
    }


# ✅ 3.1 Portfolio Summary Download
@router.get("/portfolio/download")
def download_portfolio_summary(
    format: str = Query("pdf", enum=["pdf", "excel"]),
    db: Session = Depends(get_db),
    current_investor: dict = Depends(verify_token)
):
    investor_id = int(current_investor["sub"])

    data = [
        {"Scheme": "HDFC Equity", "Amount": 10000, "Units": 105.23},
        {"Scheme": "SBI Bluechip", "Amount": 5000, "Units": 48.60},
    ]
    df = pd.DataFrame(data)

    folder = "downloads"
    os.makedirs(folder, exist_ok=True)

    if format == "excel":
        file_path = f"{folder}/portfolio_{investor_id}.xlsx"
        df.to_excel(file_path, index=False)
    else:
        file_path = f"{folder}/portfolio_{investor_id}.pdf"
        with open(file_path, "w") as f:
            f.write(df.to_string(index=False))

    return FileResponse(
        path=file_path,
        filename=os.path.basename(file_path),
        media_type="application/octet-stream"
    )


# ✅ 4. Create New Request (SIP/Redemption/etc)
@router.post("/requests")
def create_request(
    request_data: dict,
    db: Session = Depends(get_db),
    current_investor: dict = Depends(verify_token)
):
    return {
        "status": "success",
        "message": f"Your {request_data.get('type')} request has been recorded."
    }


# ✅ 5. Investor Alerts (KYC/FATCA/Nomination)
@router.get("/alerts")
def investor_alerts(
    db: Session = Depends(get_db),
    current_investor: dict = Depends(verify_token)
):
    return {
        "kyc_alert": False,
        "fatca_alert": True,
        "nomination_alert": False
    }


# ✅ 6. Transaction History with Filters
@router.get("/transactions")
def transaction_history(
    txn_type: Optional[str] = Query(None, description="Filter by type (SIP, Lumpsum, Redemption)"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    current_investor: dict = Depends(verify_token)
):
    transactions = [
        {"type": "SIP", "amount": 5000, "date": "2024-05-01"},
        {"type": "Lumpsum", "amount": 25000, "date": "2024-04-12"},
        {"type": "Redemption", "amount": 10000, "date": "2024-03-30"},
        {"type": "SIP", "amount": 3000, "date": "2024-03-01"},
    ]

    if txn_type:
        transactions = [t for t in transactions if t["type"].lower() == txn_type.lower()]
    if start_date:
        transactions = [t for t in transactions if t["date"] >= start_date]
    if end_date:
        transactions = [t for t in transactions if t["date"] <= end_date]

    return transactions


# ✅ 7. Logout from all devices / Token revoke (mock)
@router.post("/logout")
def logout_all_devices(
    current_investor: dict = Depends(verify_token)
):
    # In real use: store/revoke tokens in database or blacklist
    return {
        "status": "success",
        "message": "Logged out from all devices."
    }
