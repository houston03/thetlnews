from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.core.database import get_db
from src.app.services.promocode import validate_promo_code
from src.app.models.record import Record
from src.app.schemas.promocode import PromoCodeRequest, PromoCodeResponse
from sqlalchemy.future import select


promocode_router = APIRouter(prefix="/promocode", tags=["Promo Code"])

@promocode_router.post("/{record_id}", response_model=PromoCodeResponse)
async def validate_code(
    record_id: int,
    promo_code_request: PromoCodeRequest,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Record).filter(Record.id == record_id))
    record = result.scalars().first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    extended_description = await validate_promo_code(promo_code_request.promo_code, record)
    return PromoCodeResponse(extended_description=extended_description)
