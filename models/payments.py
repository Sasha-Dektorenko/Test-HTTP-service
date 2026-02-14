from sqlalchemy import ForeignKey, String, Date, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.db import Base
from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .credits import Credit
    from .dictionary import Dictionary

class Payment(Base):
    __tablename__ = 'payments'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sum: Mapped[float] = mapped_column(nullable=False)
    payment_date: Mapped[date] = mapped_column(Date, nullable=False)
    credit_id: Mapped[int] = mapped_column(Integer, ForeignKey('credits.id'), nullable=False)
    type_id: Mapped[int] = mapped_column(Integer, ForeignKey('dictionary.id'), nullable=False)
    
    credit: Mapped["Credit"] = relationship("Credit", back_populates="payments")
    dictionary: Mapped["Dictionary"] = relationship("Dictionary")