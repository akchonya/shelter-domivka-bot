"""Import all routers and add them to routers_list."""
from .admin import router as admin_router
from .user import router as user_router
from .test import router as test_router


routers_list = [admin_router, user_router, test_router]

__all__ = [
    "routers_list",
]
