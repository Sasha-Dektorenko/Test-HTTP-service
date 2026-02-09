from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database.db import Base
from uuid import uuid4
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .credits import Credit

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    login: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    registation_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    credits: Mapped[list["Credit"]] = relationship("Credit", back_populates="user", cascade="all, delete-orphan")