from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Database setup
from app.database import Base, engine
Base.metadata.create_all(bind=engine)

# Import routers
from app.routes.admin import router as admin_router
from app.routes.client import router as client_router
from app.routes.distributor import router as distributor_router

# FastAPI instance
app = FastAPI(
    title="SAAMPD Mutual Fund Backend",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(client_router, prefix="/client", tags=["Client"])
app.include_router(distributor_router, prefix="/distributor", tags=["Distributor"])

# Root route
@app.get("/")
def root():
    return {"message": "SAAMPD API is running"}
