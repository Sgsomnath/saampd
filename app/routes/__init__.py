from .admin import router as admin_router
from .investor import router as investor_router
from .distributor import router as distributor_router

__all__ = ["admin_router", "investor_router", "distributor_router"]