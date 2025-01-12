from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from fastapi import HTTPException, status
from src.app.models.cart import Cart
from src.app.models.record import Record


async def add_to_cart(db: AsyncSession, user_id: int, record_id: int):
    # Проверяем, существует ли запись
    result = await db.execute(select(Record).filter(Record.id == record_id))
    record = result.scalars().first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")

    # Добавляем запись в корзину
    cart_item = Cart(user_id=user_id, record_id=record_id)
    db.add(cart_item)
    await db.commit()
    await db.refresh(cart_item)
    return cart_item


async def get_cart(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(Cart).options(joinedload(Cart.record)).filter(Cart.user_id == user_id)
    )
    return result.scalars().all()


async def remove_from_cart(db: AsyncSession, user_id: int, cart_id: int):
    result = await db.execute(select(Cart).filter(Cart.id == cart_id, Cart.user_id == user_id))
    cart_item = result.scalars().first()
    if not cart_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")

    await db.delete(cart_item)
    await db.commit()
