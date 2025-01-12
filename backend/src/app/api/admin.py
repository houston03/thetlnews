from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.app.core.database import get_db
from src.app.services.user import get_current_admin
from src.app.models.record import Record
from src.app.schemas.record import RecordCreate, RecordUpdate, RecordResponse

admin_router = APIRouter(prefix="/admin", tags=["Admin"])

@admin_router.post("/add-record", response_model=RecordResponse)
async def add_record(record_data: RecordCreate, db: AsyncSession = Depends(get_db), admin=Depends(get_current_admin)):
    try:
        # Создаем новую запись
        new_record = Record(**record_data.dict())
        db.add(new_record)
        await db.commit()
        await db.refresh(new_record)
        return new_record
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@admin_router.put("/edit-record/{record_id}", response_model=RecordResponse)
async def edit_record(
    record_id: int,
    record_data: RecordUpdate,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin)
):
    try:
        # Проверяем, существует ли запись
        result = await db.execute(select(Record).where(Record.id == record_id))
        record = result.scalars().first()
        if not record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")

        # Обновляем запись
        for key, value in record_data.dict(exclude_unset=True).items():
            setattr(record, key, value)

        await db.commit()
        await db.refresh(record)
        return record
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
