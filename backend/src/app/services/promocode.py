from fastapi import HTTPException, status
from src.app.models.record import Record


PROMO_CODES = {
    "hBuhD23m": "This is a free extended description.",
    "bqSWr26w": "This is a VIP extended description."
}

async def validate_promo_code(promo_code: str, record: Record):
    extended_description = PROMO_CODES.get(promo_code)
    if not extended_description:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid promo code")
    return extended_description
