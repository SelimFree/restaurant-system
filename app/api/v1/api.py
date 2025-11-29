from fastapi import APIRouter
from api.v1.endpoints import realtime, auth

api_router = APIRouter()

api_router.include_router(realtime.router, tags=["Real-time"])
api_router.include_router(auth.router, tags=["Auth"])

# Simple health check
@api_router.get("/health", tags=["Default"])
async def health_check():
    return {"status": "ok", "version": "v1"}