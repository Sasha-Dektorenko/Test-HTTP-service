from sqlalchemy import ForeignKey, String, Date, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.db import Base
from datetime import date
from typing import TYPE_CHECKING 

if TYPE_CHECKING:
    from .users import User
    from .dictionary import Dictionary
    from .payments import Payment

class Credit(Base):
    __tablename__ = 'credits'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    issuance_date: Mapped[date] = mapped_column(Date, nullable=False)
    return_date: Mapped[date] = mapped_column(Date, nullable=False)
    actual_return_date: Mapped[date] = mapped_column(Date, nullable=True)
    body: Mapped[float] = mapped_column(nullable=False)
    percent: Mapped[float] = mapped_column(nullable=False)
    
    user: Mapped["User"] = relationship("User", back_populates="credits")
    payments: Mapped[list["Payment"]] = relationship("Payment", back_populates="credit", cascade="all, delete-orphan")
    