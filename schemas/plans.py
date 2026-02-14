from pydantic import BaseModel
from datetime import date 


class PlanPerformance_3(BaseModel):
    period: date
    category: str
    sum: float
    credits_sum: float
    percentage: float
    model_config = {"from_attributes": True}
    
class PlanPerformance_4(BaseModel):
    period: date
    category: str
    sum: float
    payments_sum: float
    percentage: float
    model_config = {"from_attributes": True}