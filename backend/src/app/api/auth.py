from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from src.app.core.database import get_db
from src.app.schemas.auth import UserCreate, LoginRequest, Token
from src.app.services.user import create_user, authenticate_user
from src.app.core.security import create_access_token
from src.app.tasks.send_email import send_email

# from src.app.models import User
# from src.app.schemas.user import UserProfileResponse
import logging

logger = logging.getLogger(__name__)

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        logger.info(f"Registering user: {user.email}")
        await create_user(db, user)  # Используем await

        send_email.delay(
            to_email=user.email,
            subject="Welcome to TheTL!",
            message=f"Hello {user.nickname},\n\nThank you for registering at TheTL. We're excited to have you on board!"
        )
        return {"message": "User registered successfully."}
    except ValueError as e:
        logger.error(f"ValueError: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")


@auth_router.post("/login", response_model=Token)
async def login(login_request: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, login_request.email, login_request.password)  # Используем await
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


# @auth_router.get("/profile", response_model=UserProfileResponse)
# async def get_user_profile(
#     current_user: User = Depends(get_current_user),
# ):
#     return current_user
