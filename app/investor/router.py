from fastapi import APIRouter

router = APIRouter(prefix="/investor", tags=["Investor"])

@router.get("/")
def investor_home():
    return {"message": "Welcome to the Investor API"}
