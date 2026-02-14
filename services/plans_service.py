from sqlalchemy.ext.asyncio import AsyncSession
from models import Plan
from database.uow import get_uow
from fastapi import Depends, HTTPException
from database.db import get_session
import pandas as pd
from fastapi import UploadFile
import io
from datetime import date
from schemas.plans import PlanPerformance_3, PlanPerformance_4
from schemas.performance import MonthPerformance


def get_plans_service(session: AsyncSession = Depends(get_session)) -> "PlansService":
    return PlansService(session)

class PlansService():
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def insert_plans(self, file: UploadFile):
        async with get_uow(self.session) as uow:
            content = await file.read()
            try:
                df = pd.read_excel(io.BytesIO(content))
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error reading Excel file: {str(e)}")
            
            df["period"] = pd.to_datetime(df["period"], dayfirst=True)
            
            
            if df["period"].isnull().any():
                raise HTTPException(status_code=400, detail="Period column contains null values")
            
            
            if not (getattr(df["period"].dt, "day") == 1).all():
                raise HTTPException(status_code=400, detail="Period column must contain the first day of each month")
            
            df["sum"].fillna(0, inplace=True)
            plans = []
            for row in df.itertuples(index=False):
                
                plan = Plan(
                    period=row.period,
                    sum=row.sum,
                    category_id=row.category_id
                )
                if await uow.plan_repo.plan_exists(plan.period, plan.category_id):
                    raise HTTPException(status_code=400, detail="Plan for this month and category already exists")
                
                plans.append(plan)
                
            await uow.plan_repo.insert_plans(plans)
            
        return f"Inserted {len(plans)} plans successfully"
    
    async def plans_performance(self, date: date):
        async with get_uow(self.session) as uow:
            try:
                period = pd.to_datetime(date, dayfirst=True)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error parsing date: {str(e)}")
            
            plans = await uow.plan_repo.get_plans_by_date(period)
            if not plans:
                raise HTTPException(status_code=404, detail="No plans found for this month")
            
            performance = []
            for plan in plans:
                if plan.category_id == 3:
                    credits = await uow.credit_repo.get_credits_by_month(plan.period)
                    credits_sum = sum(credit.body for credit in credits)
                    performance.append(PlanPerformance_3.model_validate({
                        "period": plan.period,
                        "category": plan.dictionary.name if plan.dictionary else "N/A",
                        "sum": plan.sum,
                        "credits_sum": credits_sum,
                        "percentage": (credits_sum / plan.sum * 100) if plan.sum else 0
                    }))
                elif plan.category_id == 4:
                    payments = await uow.payment_repo.get_payments_by_month(plan.period)
                    payments_sum = sum(payment.sum for payment in payments)
                    performance.append(PlanPerformance_4.model_validate(
                        {
                        "period": plan.period,
                        "category": plan.dictionary.name if plan.dictionary else "N/A",
                        "sum": plan.sum,
                        "payments_sum": payments_sum,
                        "percentage": (payments_sum / plan.sum * 100) if plan.sum else 0
                        }
                    ))
                    
            return performance
        
    # async def year_performance(self, year: int):
    #     async with get_uow(self.session) as uow:
    #         year_performance = []
    #         for month in range(1, 13):
    #             date = date(year, month, 1)
    #             plans = await uow.plan_repo.get_plans_by_date(date)
    #             payments = await uow.payment_repo.get_payments_by_month(date)
    #             credits = await uow.credit_repo.get_credits_by_month(date)
    #             issuance_sum = sum(credit.body for credit in credits)
    #             payments_sum = sum(payment.sum for payment in payments)
    #             for plan in plans:
    #                 year_performance.append(MonthPerformance.model_validate({
    #                     "date": date,
    #                     "issuance_count": len(credits), 
    #                     "plan_issuance_sum": ,
    #                     "issuance_sum": issuance_sum, 
    #                     "issuence_percentage": (issuance_sum / plan.sum * 100) if plan.sum else 0,
    #                     "payments_count": len(payments),
    #                     "payments_sum": payments_sum,
    #                     "plan_fee_sum": ,
    #                 }))
                    
                    
                    
                    
                    
                
            
            
            
            
            
            
            
            
            
            
            
            
        
        