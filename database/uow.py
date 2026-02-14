from sqlalchemy.ext.asyncio import AsyncSession
from .db import get_session
from fastapi import Depends
from repositories.users import UserRepository
from repositories.credits import CreditRepository
from repositories.plans import PlansRepository
from repositories.payments import PaymentsRepository

class Uow:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.user_repo = UserRepository(db_session)
        self.credit_repo = CreditRepository(db_session)
        self.plan_repo = PlansRepository(db_session)
        self.payment_repo = PaymentsRepository(db_session)
        
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.db_session.rollback()
        else:
            await self.db_session.commit()
        await self.db_session.close()
        
def get_uow(db_session: AsyncSession = Depends(get_session)) -> Uow:
    return Uow(db_session)
        
        