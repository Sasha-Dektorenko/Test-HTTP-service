from sqlalchemy.ext.asyncio import AsyncSession
from models import Plan
from sqlalchemy import select
from datetime import date
from sqlalchemy.orm import selectinload, joinedload


class PlansRepository():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def insert_plans(self, plans: list[Plan]):
        self.session.add_all(plans)
        await self.session.flush()

    async def plan_exists(self, period: date, category_id: int):
        stmt = select(Plan).where(Plan.period == period, Plan.category_id == category_id)
        plan = await self.session.scalars(stmt)
        return plan.first()

    async def get_plans_by_date(self, period: date):
        stmt = (
            select(Plan)
            .where(Plan.period == period)
            .options(joinedload(Plan.dictionary))  
        )
        result = await self.session.scalars(stmt)
        return result.all()
