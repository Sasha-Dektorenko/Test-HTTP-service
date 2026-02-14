from sqlalchemy import ForeignKey, String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.db import Base
from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .credits import Credit

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    registration_date: Mapped[date] = mapped_column(Date, nullable=False)
    
    credits: Mapped[list["Credit"]] = relationship("Credit", back_populates="user", cascade="all, delete-orphan")