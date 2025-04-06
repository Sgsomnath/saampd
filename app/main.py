from fastapi import FastAPI
from app.core.config.settings import settings
from app.database import engine
from app.core.models.base import Base

# Routers
from app.admin.router import router as admin_router
from app.distributor.router import router as distributor_router
from app.investor.router import router as investor_router

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="Mutual Fund Corporate Distributor App for STARSAAMPD MF DISTRIBUTORS LLP",
    version="1.0.0"
)

# Create tables at startup
Base.metadata.create_all(bind=engine)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "HELLO STARSAAMPD MF DISTRIBUTORS LLP!"}

# Register routers
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(distributor_router, prefix="/distributor", tags=["Distributor"])
app.include_router(investor_router, prefix="/investor", tags=["Investor"])
