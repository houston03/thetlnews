from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from src.app.core.database import Base


class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    record_id = Column(Integer, ForeignKey("records.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="cart")