from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from src.app.core.database import Base


class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)  # Название
    description = Column(String, nullable=False)  # Описание
    example = Column(Text, nullable=True)  # Пример
    extended_description = Column(Text, nullable=True)  # Расширенное описание
