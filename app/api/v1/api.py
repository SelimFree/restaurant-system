from fastapi import APIRouter
from .endpoints import realtime

api_router = APIRouter()

api_router.include_router(realtime.router, tags=["Real-time"])

# Simple health check
@api_router.get("/health", tags=["Default"])
async def health_check():
    return {"status": "ok", "version": "v1"}