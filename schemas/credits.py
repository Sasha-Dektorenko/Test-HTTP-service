from pydantic import BaseModel
from datetime import date

class ReturnedCredit(BaseModel):
    issuance_date: date
    is_returned: bool
    act_return_date: date
    body: int
    percents: float
    payments: float
    model_config = {"from_attributes": True}
    
class ActualCredit(BaseModel):
    issuance_date: date
    is_returned: bool
    return_date: date
    expired_days: int
    body: int
    percents: float
    body_payments: float
    percents_payments: float
    model_config = {"from_attributes": True}