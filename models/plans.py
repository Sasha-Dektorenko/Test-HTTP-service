from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database.db import Base
from uuid import uuid4
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .dictionary import Dictionary
    
class Plan(Base):
    __tablename__ = 'plans'
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    period: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    sum: Mapped[float] = mapped_column(nullable=False)
    category_id: Mapped[int] = mapped_column(nullable=False)
    
    dictionaries: Mapped[list["Dictionary"]] = relationship("Dictionary", back_populates="plan")
    
    
    
    