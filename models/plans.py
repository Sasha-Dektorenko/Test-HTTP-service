from sqlalchemy import ForeignKey, Date, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.db import Base
from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .dictionary import Dictionary
    
class Plan(Base):
    __tablename__ = 'plans'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    period: Mapped[date] = mapped_column(Date, nullable=False)
    sum: Mapped[float] = mapped_column(nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('dictionary.id'), nullable=False)
    
    dictionary: Mapped["Dictionary"] = relationship("Dictionary")