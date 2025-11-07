from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.api import api_router
from core.redis_conn import redis_client

app = FastAPI(
    title="Modular Restaurant Management Platform",
    openapi_url="/api/v1/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Connect to Redis on application startup."""
    await redis_client.connect()

@app.on_event("shutdown")
async def shutdown_event():
    """Disconnect from Redis on application shutdown."""
    await redis_client.disconnect()


app.include_router(api_router, prefix="/api/v1")


# A simple root endpoint to confirm the API is running
@app.get("/")
def read_root():
    return {"message": "Welcome to the Restaurant Management API"}