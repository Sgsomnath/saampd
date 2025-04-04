from fastapi import APIRouter

router = APIRouter(prefix="/distributor", tags=["Distributor"])

@router.get("/")
def distributor_home():
    return {"message": "Welcome to the Distributor API"}
