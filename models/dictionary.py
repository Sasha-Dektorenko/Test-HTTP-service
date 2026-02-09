from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database.db import Base
from uuid import uuid4
from typing import TYPE_CHECKING 

if TYPE_CHECKING:
    from .credits import Credit
    from .plans import Plan

class Dictionary(Base):
    __tablename__ = 'dictionary'
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    plan_id: Mapped[str] = mapped_column(String(36), ForeignKey('plans.id'), nullable=False)
    
    credit: Mapped["Credit"] = relationship("Credit", back_populates="dictionary", uselist=False)
    plan: Mapped["Plan"] = relationship("Plan", back_populates="dictionaries")
