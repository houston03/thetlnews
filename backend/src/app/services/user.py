from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from src.app.models.auth import User as UserModel
from src.app.schemas.auth import UserCreate
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from src.app.core.config import settings
from src.app.core.database import get_db


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


async def create_user(db: AsyncSession, user: UserCreate):
    # Проверяем, есть ли пользователь с таким email
    result = await db.execute(select(UserModel).filter(UserModel.email == user.email))
    if result.scalars().first():
        raise ValueError("Email already registered.")

    # Проверяем, есть ли пользователь с таким nickname
    result = await db.execute(select(UserModel).filter(UserModel.nickname == user.nickname))
    if result.scalars().first():
        raise ValueError("Nickname already taken.")

    hashed_password = get_password_hash(user.password)
    db_user = UserModel(email=user.email, nickname=user.nickname, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()  # Асинхронный commit
    await db.refresh(db_user)  # Обновление объекта
    return db_user


async def get_current_user(token: str, db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    result = await db.execute(select(UserModel).filter(UserModel.email == email))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not found")

    return user


async def create_admin_user(db: AsyncSession, email: str, password: str):
    result = await db.execute(select(UserModel).filter(UserModel.email == email))
    admin_user = result.scalars().first()

    # Если администратор уже существует, ничего не делаем
    if admin_user:
        return

    # Создаем администратора
    hashed_password = get_password_hash(password)
    admin_user = UserModel(email=email, nickname="admin", hashed_password=hashed_password, is_admin=True)
    db.add(admin_user)
    await db.commit()
    await db.refresh(admin_user)


async def get_current_admin(token: str, db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    result = await db.execute(select(UserModel).filter(UserModel.email == email))
    user = result.scalars().first()
    if not user or not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    return user


async def authenticate_user(db: AsyncSession, email: str, password: str):
    result = await db.execute(select(UserModel).filter(UserModel.email == email))
    user = result.scalars().first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
