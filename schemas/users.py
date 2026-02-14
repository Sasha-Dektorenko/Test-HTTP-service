from pydantic import BaseModel
from datetime import date 
from schemas.credits import ReturnedCredit, ActualCredit

class UserCredits(BaseModel):
    id: int
    login: str
    registration_date: date
    returned_credits: list[ReturnedCredit]
    actual_credits: list[ActualCredit]
    model_config = {"from_attributes": True}
    

    
    