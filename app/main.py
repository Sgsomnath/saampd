from fastapi import FastAPI
from app.core.config.settings import settings
from app.core.database.session import engine
from app.core.models.base import Base

# Routers import
from app.admin.router import router as admin_router
from app.distributor.router import router as distributor_router
from app.investor.router import router as investor_router

# Create FastAPI instance
app = FastAPI(
    title=settings.app_name,
    description="Mutual Fund Corporate Distributor App for STARSAAMPD MF DISTRIBUTORS LLP",
    version="1.0.0"
)

# Create all database tables on startup
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "HELLO STARSAAMPD MF DISTRIBUTORS LLP!"}

# Include routers
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(distributor_router, prefix="/distributor", tags=["Distributor"])
app.include_router(investor_router, prefix="/investor", tags=["Investor"])
