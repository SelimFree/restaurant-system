from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from db.database import get_db
from models.menus import Menu
from models.users import User
from schemas.menus import MenuCreate, MenuRead, MenuUpdate
from api.deps import role_required

router = APIRouter()


# GET ALL MENUS FOR A RESTAURANT
@router.get("/menus/{restaurant_id}", response_model=List[MenuRead])
async def get_menus(
    restaurant_id: int,
    current_user: User = Depends(role_required(["admin", "manager", "waiter"])),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Menu).where(Menu.restaurant_id == restaurant_id))
    menus = result.scalars().all()
    return menus


# CREATE MENU
@router.post("/menus", response_model=MenuRead)
async def create_menu(
    menu_in: MenuCreate,
    current_user: User = Depends(role_required(["admin", "manager"])),
    db: AsyncSession = Depends(get_db)
):
    new_menu = Menu(
        restaurant_id=menu_in.restaurant_id,
        name=menu_in.name
    )
    db.add(new_menu)
    await db.commit()
    await db.refresh(new_menu)
    return new_menu


# UPDATE MENU
@router.patch("/menus/{menu_id}", response_model=MenuRead)
async def update_menu(
    menu_id: int,
    data: MenuUpdate,
    current_user: User = Depends(role_required(["admin", "manager"])),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Menu).where(Menu.id == menu_id))
    menu = result.scalars().first()

    if not menu:
        raise HTTPException(404, "Menu not found")

    if data.name is not None:
        menu.name = data.name

    await db.commit()
    await db.refresh(menu)
    return menu


# DELETE MENU
@router.delete("/menus/{menu_id}")
async def delete_menu(
    menu_id: int,
    current_user: User = Depends(role_required(["admin"])),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Menu).where(Menu.id == menu_id))
    menu = result.scalars().first()

    if not menu:
        raise HTTPException(404, "Menu not found")

    await db.delete(menu)
    await db.commit()

    return {"message": "Menu deleted"}
