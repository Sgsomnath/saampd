from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.core.config.settings import settings
from app.core.database.session import engine
from app.core.models.base import Base

from jwt_auth.dependencies import verify_token

# 🔹 Base Routers
from app.admin.router import router as admin_router
from app.distributor.router import router as distributor_router
from app.investor.router import router as investor_router

# 🔹 Admin Routers
from app.admin.dashboard_router import router as dashboard_router
from app.admin.distributor_router import router as admin_distributor_router 
from app.admin.investor_router import router as admin_investor_router # ✅ NEW

# 🔹 Distributor Routers
from app.distributor.dashboard_router import router as distributor_dashboard_router
from app.distributor.investor_router import router as distributor_investor_router
from app.distributor.commission_router import router as distributor_commission_router
from app.distributor.report_router import router as distributor_report_router
from app.distributor.document_router import router as distributor_document_router
from app.distributor.message_router import router as distributor_message_router
from app.distributor.twofa_router import router as distributor_twofa_router
from app.distributor.commission_chart_router import router as commission_chart_router
from app.distributor.profile_router import router as distributor_profile_router

# 🔹 Investor Routers
from app.investor.dashboard_router import router as investor_dashboard_router
from app.investor.profile_router import router as investor_profile_router
from app.investor.twofa_router import router as investor_twofa_router
from app.investor.logout_router import router as investor_logout_router
from app.investor.avatar_router import router as investor_avatar_router

# 🔷 FastAPI instance
app = FastAPI(
    title=settings.app_name,
    description="Mutual Fund Corporate Distributor App for STARSAAMPD MF DISTRIBUTORS LLP",
    version="1.0.0"
)

# 🔷 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ Production e specific domain use korben
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔷 DB Table Create
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# 🔷 Root route
@app.get("/")
def root():
    return {"message": "SAAMPD API is running"}

# 🔐 Secure test route
@app.get("/secure-test", dependencies=[Depends(verify_token)])
def secure_test():
    return {"message": "✅ Token valid. Secure access granted!"}

# 🔷 Register All Routers

# Admin
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(dashboard_router)  # Admin Dashboard
app.include_router(admin_distributor_router)  # ✅ Admin can view distributors
app.include_router(admin_investor_router)

# Distributor
app.include_router(distributor_router, prefix="/distributor", tags=["Distributor"])
app.include_router(distributor_dashboard_router)  # Dashboard
app.include_router(distributor_profile_router)    # Profile
app.include_router(distributor_investor_router)   # Investor Management
app.include_router(distributor_commission_router) # Commission
app.include_router(distributor_report_router)     # Reports
app.include_router(distributor_document_router)   # Documents
app.include_router(distributor_message_router)    # Messages
app.include_router(commission_chart_router)       # Chart
app.include_router(distributor_twofa_router)      # 2FA

# Investor
app.include_router(investor_router, prefix="/investor", tags=["Investor"])
app.include_router(investor_dashboard_router)
app.include_router(investor_profile_router)
app.include_router(investor_twofa_router)
app.include_router(investor_logout_router)
app.include_router(investor_avatar_router)
