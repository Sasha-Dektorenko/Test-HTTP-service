from sqlalchemy.ext.asyncio import AsyncSession
from models import User

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id: int):
        user = await self.session.get(User, user_id)
        return user
    
    
       