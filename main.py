# app/main.py

from fastapi import FastAPI
from app.core.config.settings import settings

# Routers import
from app.admin.router import router as admin_router
from app.distributor.router import router as distributor_router
from app.investor.router import router as investor_router

app = FastAPI(
    title="SAAMPD Backend",
    description="Mutual Fund Corporate Distributor App for STARSAAMPD MF DISTRIBUTORS LLP",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "HELLO STARSAAMPD MF DISTRIBUTORS LLP!"}

# Include all routers
app.include_router(admin_router)
app.include_router(distributor_router)
app.include_router(investor_router)
