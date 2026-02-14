from sqlalchemy.ext.asyncio import AsyncSession
from models import Payment
from sqlalchemy import select
from typing import Sequence
from sqlalchemy.orm import selectinload
from datetime import date
import pandas as pd



class PaymentsRepository():
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_payments_by_month(self, period: date):
        stmt = (
                select(Payment)
                .where(
                    Payment.payment_date >= pd.to_datetime(period).replace(day=1),
                    Payment.payment_date < (pd.to_datetime(period).replace(day=1) + pd.DateOffset(months=1))
                ))
        result = await self.session.scalars(stmt)
        return result.all()
    
   
        
