from fastapi import APIRouter
from api.v1.endpoints import realtime, auth, restaurants, menus, menu_items, tables, orders, users

api_router = APIRouter()

api_router.include_router(realtime.router, tags=["Real-time"])
api_router.include_router(auth.router, tags=["Auth"])
api_router.include_router(users.router, tags=["Users"])
api_router.include_router(restaurants.router, tags=["Restaurants"])
api_router.include_router(menus.router, tags=["Menus"])
api_router.include_router(menu_items.router, tags=["Menu Items"])
api_router.include_router(tables.router, tags=["Tables"])
api_router.include_router(orders.router, tags=["Orders and Order Items"])

# Simple health check
@api_router.get("/health", tags=["Default"])
async def health_check():
    return {"status": "ok", "version": "v1"}