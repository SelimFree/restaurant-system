from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from db.database import get_db
from models.users import User
from schemas.users import UserRole, UserCreate, UserRead, UserUpdate
from api.deps import role_required
from core import security

router = APIRouter()

@router.get("/users", response_model=List[UserRead])
async def get_all_users(
    current_user: User = Depends(role_required([UserRole.ADMIN.value, UserRole.MANAGER.value])),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(User)
    result = await db.execute(stmt)
    users = result.scalars().all()
    return users

# GET SINGLE USER
@router.get("/users/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    current_user: User = Depends(role_required([UserRole.ADMIN.value, UserRole.MANAGER.value])),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalars().first()

    if not user:
        raise HTTPException(404, "User not found")

    return user


# CREATE RESTAURANT
@router.post("/users", response_model=UserRead)
async def create_user(
    user_in: UserCreate,
    current_user: User = Depends(role_required([UserRole.ADMIN.value])),
    db: AsyncSession = Depends(get_db)
):
    
    result = await db.execute(select(User).where(User.email == user_in.email))
    existing_user = result.scalars().first()
    
    if existing_user:
        raise HTTPException(
            status_code=400, 
            detail="Email already registered"
        )
    
    hashed_pw = security.get_password_hash(user_in.password)
    new_user = User(
        name=user_in.name,
        email=user_in.email,
        phone=user_in.phone,
        role=user_in.role.value,
        hashed_password=hashed_pw,
        meta=user_in.meta
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


# UPDATE USER
@router.patch("/users/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    data: UserUpdate,
    current_user: User = Depends(role_required([UserRole.ADMIN.value])),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalars().first()

    if not user:
        raise HTTPException(404, "User not found")

    if data.name is not None:
        user.name = data.name

    if data.role is not None:
        user.role = data.role.value

    if data.password is not None:
        hashed_pw = security.get_password_hash(data.password)
        user.hashed_password = hashed_pw

    if data.phone is not None:
        user.phone = data.phone
        
    if data.meta is not None:
        user.meta = data.meta

    await db.commit()
    await db.refresh(user)

    return user


# DELETE RESTAURANT
@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(role_required([UserRole.ADMIN.value])),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalars().first()

    if not user:
        raise HTTPException(404, "User not found")

    await db.delete(user)
    await db.commit()

    return {"message": "User deleted"}