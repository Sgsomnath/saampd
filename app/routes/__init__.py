from .admin import router as admin_router
from .client import router as client_router
from .distributor import router as distributor_router

__all__ = ["admin_router", "client_router", "distributor_router"]