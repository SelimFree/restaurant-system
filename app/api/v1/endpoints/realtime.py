import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from core.redis_conn import redis_client

router = APIRouter()


# test websocker endpoint, to be changed later during the development
@router.websocket("/ws/orders/{restaurant_id}")
async def websocket_order_updates(
    websocket: WebSocket,
    restaurant_id: str,
    token: str = Query(...)
):
    """
    WebSocket endpoint for real-time order status updates.
    """
    
    await websocket.accept()
    print(f"WebSocket connection accepted for restaurant: {restaurant_id}")

    channel_name = f"restaurant:{restaurant_id}:orders"
    pubsub = await redis_client.subscribe(channel_name)
    
    if not pubsub:
        await websocket.close(code=1011, reason="Could not connect to real-time service")
        return

    # Task to listen for Redis messages and send to client
    async def redis_listener(ws: WebSocket):
        try:
            while True:
                message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                if message:
                    print(f"Sending message to client: {message['data']}")
                    await ws.send_text(message['data'])
        except Exception as e:
            print(f"Redis listener error: {e}")
        finally:
            print("Redis listener task finished.")

    # Task to listen for messages from the client
    async def client_listener(ws: WebSocket):
        try:
            while True:
                await ws.receive_text()
        except WebSocketDisconnect:
            print(f"Client disconnected from {restaurant_id}")
        except Exception as e:
            print(f"Client listener error: {e}")
        finally:
            print("Client listener task finished.")

    # Run both tasks concurrently
    try:
        listener_task = asyncio.create_task(redis_listener(websocket))
        client_task = asyncio.create_task(client_listener(websocket))
        
        done, pending = await asyncio.wait(
            [listener_task, client_task],
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()
            
    finally:
        if pubsub:
            await pubsub.unsubscribe(channel_name)
            await pubsub.close()
        print(f"WebSocket connection closed for restaurant: {restaurant_id}")