from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import timedelta

from core.config import settings
from schemas.users import UserBase, UserCreate, UserLogin, Token
from models.users import User
from core import security
from db.database import get_db

router = APIRouter()

@router.post("/register", response_model=UserBase)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
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
        role=user_in.role.value,
        hashed_password=hashed_pw
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_credentials.email))
    user = result.scalars().first()

    if user:
            print(f"Trying to match input: '{user_credentials.password}'")
            print(f"Against DB Hash: '{user.hashed_password}'")
            is_valid = security.verify_password(user_credentials.password, user.hashed_password)
            print(f"Result: {is_valid}")
            
    if not user or not security.verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email, "role": user.role},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }