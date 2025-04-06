from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Correct imports for routers
from app.routes.admin import router as admin_router
from app.routes.client import router as client_router
from app.routes.distributor import router as distributor_router

# If you use database:
from app.database import Base, engine

# Auto-create tables
Base.metadata.create_all(bind=engine)

# FastAPI instance
app = FastAPI(
    title="SAAMPD Mutual Fund Backend",
)

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(client_router, prefix="/client", tags=["Client"])
app.include_router(distributor_router, prefix="/distributor", tags=["Distributor"])

# Root route
@app.get("/")
def root():
    return {"message": "SAAMPD API is running"}
