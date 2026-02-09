from sqlalchemy.ext.asyncio import AsyncSession
from .db import get_session
from fastapi import Depends

class Uow:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        
    async def __aenter__(self):
        return self.db_session
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.db_session.rollback()
        else:
            await self.db_session.commit()
        await self.db_session.close()
        
def get_uow(db_session: AsyncSession = Depends(get_session)) -> Uow:
    return Uow(db_session)
        
        