# app/distributor/report_router.py

from fastapi import APIRouter, Depends, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.database.session import get_db
from jwt_auth.dependencies import verify_token
import pandas as pd
import os

router = APIRouter(prefix="/distributor/reports", tags=["Distributor Reports"])

@router.get("/export")
def export_report(
    format: str = Query("excel", enum=["excel", "csv"]),
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    data = [
        {"Investor": "Amitava", "Investment": 50000, "Commission": 500},
        {"Investor": "Rita", "Investment": 75000, "Commission": 800},
    ]
    df = pd.DataFrame(data)

    folder = "downloads"
    os.makedirs(folder, exist_ok=True)

    file_path = f"{folder}/report.{format}"
    if format == "csv":
        df.to_csv(file_path, index=False)
    else:
        df.to_excel(file_path, index=False)

    return FileResponse(path=file_path, filename=f"report.{format}")
