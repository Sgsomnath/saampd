from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.core.config.settings import settings
from app.core.database.session import engine
from app.core.models.base import Base

from jwt_auth.dependencies import verify_token

# Routers
from app.admin.router import router as admin_router
from app.distributor.router import router as distributor_router
from app.investor.router import router as investor_router
from app.admin.dashboard_router import router as dashboard_router  # ✅ Admin dashboard router

# FastAPI instance
app = FastAPI(
    title=settings.app_name,
    description="Mutual Fund Corporate Distributor App for STARSAAMPD MF DISTRIBUTORS LLP",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ✅ In production, use specific origins only!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB auto-create on startup
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# Root Route
@app.get("/")
def root():
    return {"message": "SAAMPD API is running"}

# JWT-Protected Route (for testing)
@app.get("/secure-test", dependencies=[Depends(verify_token)])
def secure_test():
    return {"message": "✅ Token valid. Secure access granted!"}

# Register Routers
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(distributor_router, prefix="/distributor", tags=["Distributor"])
app.include_router(investor_router, prefix="/investor", tags=["Investor"])
app.include_router(dashboard_router)  # ✅ Admin dashboard routes
