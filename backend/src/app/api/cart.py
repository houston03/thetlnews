from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.core.database import get_db
from src.app.services.cart import add_to_cart, get_cart, remove_from_cart
from src.app.schemas.cart import CartAdd, CartResponse
from src.app.services.user import get_current_user

cart_router = APIRouter(prefix="/cart", tags=["Cart"])

@cart_router.post("/", response_model=CartResponse)
async def add_record_to_cart(cart_data: CartAdd, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    return await add_to_cart(db, user.id, cart_data.record_id)

@cart_router.get("/", response_model=list[CartResponse])
async def get_user_cart(db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    return await get_cart(db, user.id)

@cart_router.delete("/{cart_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_record_from_cart(cart_id: int, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    await remove_from_cart(db, user.id, cart_id)
