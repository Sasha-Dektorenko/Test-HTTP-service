from sqlalchemy.ext.asyncio import AsyncSession
from models import Credit
from sqlalchemy import select
from typing import Sequence
from sqlalchemy.orm import selectinload
from datetime import date
import pandas as pd

class CreditRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_credits(self, user_id: int) -> Sequence[Credit]:
        
        stmt = (
            select(Credit)
            .where(Credit.user_id == user_id)
            .options(selectinload(Credit.payments))
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_credits_by_month(self, period: date) -> Sequence[Credit]:
        stmt = (
            select(Credit)
            .where(
                Credit.issuance_date >= pd.to_datetime(period).replace(day=1),
                Credit.issuance_date < (pd.to_datetime(period).replace(day=1) + pd.DateOffset(months=1))
            )
            .options(selectinload(Credit.payments))
        )
        result = await self.session.scalars(stmt)
        return result.all()
         
        