from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, status
from jose import jwt, JWTError
from core.config import settings

from models.users import User
from schemas.users import UserRole
from core.redis_conn import redis_client

router = APIRouter()

async def validate_ws_user(token: str, required_roles: list = None) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        
        if email is None:
            return None
            
        if required_roles and role not in required_roles:
            print(f"Authorization failed: Role '{role}' not in {required_roles}")
            return None
            
        return User(email=email, role=role)
        
    except JWTError:
        return None

@router.websocket("/ws/orders/{restaurant_id}")
async def websocket_order_updates(
    websocket: WebSocket,
    restaurant_id: str,
    token: str = Query(...)
):
    user = await validate_ws_user(token, required_roles=[UserRole.ADMIN.value, UserRole.WAITER.value, UserRole.COOK.value])
    
    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.accept()
    print(f"User {user.email} ({user.role}) subscribed to Restaurant {restaurant_id}")

    channel_name = f"restaurant:{restaurant_id}:orders"
    pubsub = await redis_client.subscribe(channel_name)
    
    try:
        async for message in pubsub.listen():
            if message["type"] == "message":
                await websocket.send_text(message["data"])
                
    except WebSocketDisconnect:
        print(f"Client disconnected")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if pubsub:
            await pubsub.unsubscribe(channel_name)