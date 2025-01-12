from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.orm import relationship
from src.app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    nickname = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    role = Column(String, default="user")  # Роль пользователя: 'user' или 'admin' УДАЛИТЬ этот файл

    cart = relationship("Cart", back_populates="user", cascade="all, delete-orphan")