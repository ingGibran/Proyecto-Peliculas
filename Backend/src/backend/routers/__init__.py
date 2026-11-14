from .movies import router as movies_router
from .favorites import router as favorites_router
from .purchase import router as purchase_router
from .rent import router as rent_router
from .users import router as users_router

__all__ = ["favorites_router", "movies_router", "purchase_router", "rent_router", "users_router"]
