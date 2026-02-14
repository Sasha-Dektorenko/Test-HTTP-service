from pydantic import BaseModel
from datetime import date



class MonthPerformance(BaseModel):
    date: date
    issuance_count: int
    plan_issuance_sum: float
    issuance_sum: float
    issuence_percentage: float
    payments_count: int
    payments_sum: float
    plan_fee_sum: float
    issuance_sum: float
    fee_percentage: float
    issuance_month_per_year_percentage: float
    payments_month_per_year_percentage: float
    
    