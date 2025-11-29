from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from db.database import get_db
from models.restaurants import Restaurant
from models.users import User
from schemas.restaurants import RestaurantRead
from api.deps import role_required

router = APIRouter()

@router.get("/restaurants", response_model=List[RestaurantRead])
async def get_all_restaurants(
    current_user: User = Depends(role_required(["admin", "manager"])),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Restaurant)
    result = await db.execute(stmt)
    restaurants = result.scalars().all()
    return restaurants

# GET SINGLE RESTAURANT
@router.get("/restaurants/{restaurant_id}", response_model=RestaurantRead)
async def get_restaurant(
    restaurant_id: int,
    current_user: User = Depends(role_required(["admin", "manager"])),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Restaurant).where(Restaurant.id == restaurant_id)
    )
    restaurant = result.scalars().first()

    if not restaurant:
        raise HTTPException(404, "Restaurant not found")

    return restaurant


# CREATE RESTAURANT
@router.post("/restaurants", response_model=RestaurantRead)
async def create_restaurant(
    restaurant_in: RestaurantCreate,
    current_user: User = Depends(role_required(["admin"])),
    db: AsyncSession = Depends(get_db)
):
    new_restaurant = Restaurant(
        name=restaurant_in.name,
        address=restaurant_in.address,
        settings=restaurant_in.settings
    )

    db.add(new_restaurant)
    await db.commit()
    await db.refresh(new_restaurant)

    return new_restaurant


# UPDATE RESTAURANT
@router.patch("/restaurants/{restaurant_id}", response_model=RestaurantRead)
async def update_restaurant(
    restaurant_id: int,
    data: RestaurantUpdate,
    current_user: User = Depends(role_required(["admin"])),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Restaurant).where(Restaurant.id == restaurant_id)
    )
    restaurant = result.scalars().first()

    if not restaurant:
        raise HTTPException(404, "Restaurant not found")

    if data.name is not None:
        restaurant.name = data.name

    if data.address is not None:
        restaurant.address = data.address

    if data.settings is not None:
        restaurant.settings = data.settings

    await db.commit()
    await db.refresh(restaurant)

    return restaurant


# DELETE RESTAURANT
@router.delete("/restaurants/{restaurant_id}")
async def delete_restaurant(
    restaurant_id: int,
    current_user: User = Depends(role_required(["admin"])),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Restaurant).where(Restaurant.id == restaurant_id)
    )
    restaurant = result.scalars().first()

    if not restaurant:
        raise HTTPException(404, "Restaurant not found")

    await db.delete(restaurant)
    await db.commit()

    return {"message": "Restaurant deleted"}