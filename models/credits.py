from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database.db import Base
from uuid import uuid4
from datetime import datetime, timezone
from typing import TYPE_CHECKING 

if TYPE_CHECKING:
    from .users import User
    from .dictionary import Dictionary

class Credit(Base):
    __tablename__ = 'credits'
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey('users.id'), nullable=False)
    issuance_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    return_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    actual_return_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    body: Mapped[float] = mapped_column(nullable=False)
    percent: Mapped[float] = mapped_column(nullable=False)
    
    user: Mapped["User"] = relationship("User", back_populates="credits")
    dictionary: Mapped["Dictionary"] = relationship("Dictionary", back_populates="credit", uselist=False)
    