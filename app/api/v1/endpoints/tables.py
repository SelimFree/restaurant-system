from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from db.database import get_db
from models.tables import Table
from models.users import User
from models.restaurants import Restaurant
from schemas.tables import TableRead, TableCreate, TableUpdate
from schemas.users import UserRole
from api.deps import role_required


router = APIRouter()


# GET ALL TABLES FOR A RESTAURANT
@router.get("/tables/{restaurant_id}", response_model=List[TableRead])
async def get_tables(
    restaurant_id: int,
    current_user: User = Depends(role_required([UserRole.ADMIN.value, UserRole.MANAGER.value, UserRole.WAITER.value])),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Table).where(Table.restaurant_id == restaurant_id)
    )
    return result.scalars().all()

# CREATE A TABLE
@router.post("/tables", response_model=TableRead)
async def create_table(
    table_in: TableCreate,
    current_user: User = Depends(role_required([UserRole.ADMIN.value, UserRole.MANAGER.value])),
    db: AsyncSession = Depends(get_db)
):
    
    restaurant_query = await db.execute(
        select(Restaurant).where(Restaurant.id == table_in.restaurant_id)
    )
    
    restaurant = restaurant_query.scalars().first()

    if not restaurant:
        raise HTTPException(404, "Invalid restaurant id")
    
    new_table = Table(
        restaurant_id=table_in.restaurant_id,
        name_number=table_in.name_number,
        capacity=table_in.capacity,
        status=table_in.status.value,
    )

    db.add(new_table)
    await db.commit()
    await db.refresh(new_table)
    return new_table


# GET A SINGLE TABLE
@router.get("/table/{table_id}", response_model=TableRead)
async def get_table(
    table_id: int,
    current_user: User = Depends(role_required([UserRole.ADMIN.value, UserRole.MANAGER.value, UserRole.WAITER.value])),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Table).where(Table.id == table_id)
    )
    table = result.scalars().first()

    if not table:
        raise HTTPException(404, "Table not found")

    return table



# UPDATE A TABLE (name, capacity, status)
@router.patch("/tables/{table_id}", response_model=TableRead)
async def update_table(
    table_id: int,
    data: TableUpdate,
    current_user: User = Depends(role_required([UserRole.ADMIN.value, UserRole.MANAGER.value])),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Table).where(Table.id == table_id))
    table = result.scalars().first()

    if not table:
        raise HTTPException(404, "Table not found")

    if data.name_number is not None:
        table.name_number = data.name_number
    if data.capacity is not None:
        table.capacity = data.capacity
    if data.status is not None:
        table.status = data.status.value

    await db.commit()
    await db.refresh(table)
    return table


# DELETE A TABLE
@router.delete("/tables/{table_id}")
async def delete_table(
    table_id: int,
    current_user: User = Depends(role_required([UserRole.ADMIN.value])),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Table).where(Table.id == table_id))
    table = result.scalars().first()

    if not table:
        raise HTTPException(404, "Table not found")

    await db.delete(table)
    await db.commit()

    return {"message": "Table deleted"}
