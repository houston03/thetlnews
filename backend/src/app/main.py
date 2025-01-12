from fastapi import FastAPI
from src.app.api.auth import auth_router
from src.app.core.database import engine
from src.app.models.auth import Base
from src.app.services.user import create_admin_user
from src.app.core.config import settings
from src.app.core.database import async_session
from src.app.api.admin import admin_router
from src.app.api.cart import cart_router
from src.app.api.promocode import promocode_router

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Создаем администратора при старте
    async with async_session() as session:
        await create_admin_user(session, settings.ADMIN_EMAIL, settings.ADMIN_PASSWORD)

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(cart_router)
app.include_router(promocode_router)


# uvicorn src.app.main:app