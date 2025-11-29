from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from db.database import get_db
from models.menu_items import MenuItem
from models.users import User

from schemas.menu_items import (
    MenuItemRead,
    MenuItemCreate,
    MenuItemUpdate
)

from api.deps import role_required


router = APIRouter()


# GET ALL MENU ITEMS FOR A MENU
@router.get("/menu-items/{menu_id}", response_model=List[MenuItemRead])
async def get_menu_items(
    menu_id: int,
    current_user: User = Depends(role_required(["admin", "manager", "waiter", "cook"])),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(MenuItem).where(MenuItem.menu_id == menu_id)
    )
    return result.scalars().all()


# CREATE MENU ITEM
@router.post("/menu-items", response_model=MenuItemRead)
async def create_menu_item(
    item_in: MenuItemCreate,
    current_user: User = Depends(role_required(["admin", "manager"])),
    db: AsyncSession = Depends(get_db)
):
    new_item = MenuItem(
        menu_id=item_in.menu_id,
        name=item_in.name,
        description=item_in.description,
        price=item_in.price,
        available=item_in.available,
        prep_time=item_in.prep_time,
    )

    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item


# GET A SINGLE MENU ITEM
@router.get("/menu-item/{item_id}", response_model=MenuItemRead)
async def get_menu_item(
    item_id: int,
    current_user: User = Depends(role_required(["admin", "manager", "waiter", "cook"])),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(MenuItem).where(MenuItem.id == item_id))
    item = result.scalars().first()

    if not item:
        raise HTTPException(404, "Menu item not found")

    return item


# UPDATE MENU ITEM
@router.patch("/menu-items/{item_id}", response_model=MenuItemRead)
async def update_menu_item(
    item_id: int,
    data: MenuItemUpdate,
    current_user: User = Depends(role_required(["admin", "manager"])),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(MenuItem).where(MenuItem.id == item_id))
    item = result.scalars().first()

    if not item:
        raise HTTPException(404, "Menu item not found")

    if data.name is not None:
        item.name = data.name
    if data.description is not None:
        item.description = data.description
    if data.price is not None:
        item.price = data.price
    if data.available is not None:
        item.available = data.available
    if data.prep_time is not None:
        item.prep_time = data.prep_time

    await db.commit()
    await db.refresh(item)
    return item


# DELETE MENU ITEM
@router.delete("/menu-items/{item_id}")
async def delete_menu_item(
    item_id: int,
    current_user: User = Depends(role_required(["admin"])),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(MenuItem).where(MenuItem.id == item_id))
    item = result.scalars().first()

    if not item:
        raise HTTPException(404, "Menu item not found")

    await db.delete(item)
    await db.commit()

    return {"message": "Menu item deleted"}
