import json
from fastapi.encoders import jsonable_encoder
from core.redis_conn import redis_client

class EventType:
    ORDER_CREATED = "ORDER_CREATED"
    ORDER_UPDATED = "ORDER_UPDATED"
    ITEM_ADDED = "ITEM_ADDED"
    ITEM_UPDATED = "ITEM_UPDATED"
    ITEM_REMOVED = "ITEM_REMOVED"

async def notify_restaurant_update(restaurant_id: int, event_type: str, data: dict):
    channel = f"restaurant:{restaurant_id}:orders"
    
    payload = {
        "event": event_type,
        "restaurant_id": restaurant_id,
        "data": jsonable_encoder(data)
    }
    
    await redis_client.publish(channel, json.dumps(payload))