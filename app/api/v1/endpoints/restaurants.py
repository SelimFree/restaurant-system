from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from db.database import get_db
from models.restaurants import Restaurant
from models.users import User
from schemas.restaurants import RestaurantRead
from api.deps import get_current_user

router = APIRouter()

@router.get("/restaurants", response_model=List[RestaurantRead])
async def get_all_restaurants(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Restaurant)
    result = await db.execute(stmt)
    restaurants = result.scalars().all()
    return restaurants