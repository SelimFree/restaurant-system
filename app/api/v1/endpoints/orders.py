from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List

from db.database import get_db
from models.orders import Order
from models.order_items import OrderItem
from models.menus import Menu
from models.menu_items import MenuItem
from models.users import User
from models.tables import Table

from schemas.orders import (
    OrderCreate, OrderRead, OrderUpdate,
    OrderItemCreate, OrderItemRead, OrderStatus, OrderItemUpdate, OrderCreateMe
)
from schemas.users import UserRole
from api.deps import role_required
from services.notifications import notify_restaurant_update, EventType

router = APIRouter()


# CREATE ORDER
@router.post("/orders", response_model=OrderRead)
async def create_order(
    order_in: OrderCreate,
    current_user: User = Depends(role_required([UserRole.ADMIN.value, UserRole.WAITER.value])),
    db: AsyncSession = Depends(get_db)
):
    
    table_query = await db.execute(
        select(Table).where(Table.id == order_in.table_id)
    )
    
    table = table_query.scalars().first()

    if not table:
        raise HTTPException(404, "Invalid table id")
    
    waiter_query = await db.execute(
        select(User).where(User.id == order_in.waiter_id)
    )
    
    waiter = waiter_query.scalars().first()

    if not waiter:
        raise HTTPException(404, "Invalid waiter id")
    
    new_order = Order(
        table_id=order_in.table_id,
        waiter_id=order_in.waiter_id,
        status=OrderStatus.CREATED.value
    )

    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    
    await notify_restaurant_update(
        restaurant_id=table.restaurant_id, 
        event_type=EventType.ORDER_CREATED, 
        data=new_order
    )
    return new_order

# CREATE ORDER FOR CURRENT USER
@router.post("/orders/me", response_model=OrderRead)
async def create_order_for_me(
    order_in: OrderCreateMe,
    current_user: User = Depends(role_required([UserRole.ADMIN.value, UserRole.WAITER.value])),
    db: AsyncSession = Depends(get_db)
):
    
    table_query = await db.execute(
        select(Table).where(Table.id == order_in.table_id)
    )
    
    table = table_query.scalars().first()

    if not table:
        raise HTTPException(404, "Invalid table id")
    
    new_order = Order(
        table_id=order_in.table_id,
        waiter_id=current_user.id,
        status=OrderStatus.CREATED.value
    )

    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    
    await notify_restaurant_update(
        restaurant_id=table.restaurant_id, 
        event_type=EventType.ORDER_CREATED, 
        data=new_order
    )
    return new_order

# GET ORDERS 
@router.get("/orders", response_model=OrderRead)
async def get_orders(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(role_required([UserRole.ADMIN.value, UserRole.COOK.value]))
):
    result = await db.execute(select(Order))
    orders = result.scalars().all()

    return orders

# GET ORDER BY CURRENT USER
@router.get("/orders/me", response_model=List[OrderRead])
async def get_orders_for_me(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(role_required([UserRole.ADMIN.value, UserRole.WAITER.value]))
):
    result = await db.execute(select(Order).where(Order.waiter_id == current_user.id))
    orders = result.scalars().all()

    return orders

# GET ORDER BY ID
@router.get("/orders/{order_id}", response_model=OrderRead)
async def get_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(role_required([UserRole.ADMIN.value, UserRole.WAITER.value, UserRole.COOK.value]))
):
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalars().first()

    if not order:
        raise HTTPException(404, "Order not found")

    return order


# UPDATE ORDER STATUS
@router.patch("/orders/{order_id}", response_model=OrderRead)
async def update_order(
    order_id: int,
    data: OrderUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(role_required([UserRole.ADMIN.value, UserRole.WAITER.value, UserRole.COOK.value]))
):
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalars().first()
    if not order:
        raise HTTPException(404, "Order not found")

    table_query = await db.execute(
        select(Table).where(Table.id == order.table_id)
    )
    
    table = table_query.scalars().first()

    if data.status:
        order.status = data.status.value

    await db.commit()
    await db.refresh(order)
    
    await notify_restaurant_update(
        restaurant_id=table.restaurant_id, 
        event_type=EventType.ORDER_UPDATED, 
        data=order
    )
    return order


# ADD ORDER ITEM
@router.post("/orders/{order_id}/items", response_model=OrderItemRead)
async def add_order_item(
    order_id: int,
    item_in: OrderItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(role_required([UserRole.ADMIN.value, UserRole.WAITER.value]))
):
    menu_item_query = await db.execute(
        select(MenuItem).where(MenuItem.id == item_in.item_id)
    )
    
    menu_item = menu_item_query.scalars().first()
    
    if not menu_item:
        raise HTTPException(404, "Invalid menu item id")
    
    menu_query = await db.execute(
        select(Menu).where(Menu.id == menu_item.menu_id)
    )
    
    menu = menu_query.scalars().first()
    
    new_item = OrderItem(
        order_id=order_id,
        item_id=item_in.item_id,
        quantity=item_in.quantity,
        notes=item_in.notes
    )

    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    
    await notify_restaurant_update(
        restaurant_id=menu.restaurant_id, 
        event_type=EventType.ITEM_ADDED, 
        data=new_item
    )
    return new_item


# GET ORDER ITEMS
@router.get("/orders/{order_id}/items", response_model=List[OrderItemRead])
async def get_order_items(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(role_required([UserRole.ADMIN.value, UserRole.WAITER.value, UserRole.COOK.value]))
):
    result = await db.execute(
        select(OrderItem).where(OrderItem.order_id == order_id)
    )
    return result.scalars().all()

# UPDATE ORDER ITEM (quantity, status, notes)
@router.patch("/order-items/{item_id}", response_model=OrderItemRead)
async def update_order_item(
    item_id: int,
    data: OrderItemUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(role_required([UserRole.ADMIN.value, UserRole.WAITER.value, UserRole.COOK.value]))
):
    result = await db.execute(select(OrderItem).where(OrderItem.id == item_id))
    item = result.scalars().first()

    if not item:
        raise HTTPException(404, "Order item not found")
    
    order_query = await db.execute(
        select(Order).where(Order.id == item.order_id)
    )
    
    order = order_query.scalars().first()
    
    table_query = await db.execute(
        select(Table).where(Table.id == order.table_id)
    )
    
    table = table_query.scalars().first()

    if data.quantity is not None:
        item.quantity = data.quantity
    if data.status is not None:
        item.status = data.status.value
    if data.notes is not None:
        item.notes = data.notes

    await db.commit()
    await db.refresh(item)
    
    
    await notify_restaurant_update(
        restaurant_id=table.restaurant_id, 
        event_type=EventType.ITEM_UPDATED, 
        data=item
    )
    
    return item

# DELETE ORDER ITEM
@router.delete("/order-items/{item_id}")
async def delete_order_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(role_required([UserRole.ADMIN.value, UserRole.WAITER.value, UserRole.COOK.value]))
):
    stmt = (
        select(OrderItem)
        .options(
            selectinload(OrderItem.order).selectinload(Order.table)
        )
        .where(OrderItem.id == item_id)
    )
    result = await db.execute(stmt)
    item = result.scalars().first()

    if not item:
        raise HTTPException(404, "Order item not found")

    if not item.order or not item.order.table:
        await db.delete(item)
        await db.commit()
        return {"message": "Order item deleted (no notification sent - orphan item)"}

    restaurant_id = item.order.table.restaurant_id
    order_id = item.order_id
    deleted_item_id = item.id 

    await db.delete(item)
    await db.commit()

    await notify_restaurant_update(
        restaurant_id=restaurant_id, 
        event_type=EventType.ITEM_REMOVED, 
        data={
            "order_id": order_id, 
            "item_id": deleted_item_id
        }
    )

    return {"message": "Order item deleted"}

# GET SINGLE ORDER ITEM
@router.get("/order-item/{item_id}", response_model=OrderItemRead)
async def get_order_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(role_required([UserRole.ADMIN.value, UserRole.WAITER.value, UserRole.COOK.value]))
):
    result = await db.execute(select(OrderItem).where(OrderItem.id == item_id))
    item = result.scalars().first()

    if not item:
        raise HTTPException(404, "Order item not found")

    return item

