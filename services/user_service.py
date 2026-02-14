from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from models import User, Credit, Dictionary, Payment, Plan
from database.uow import get_uow
from schemas.users import UserCredits
from schemas.credits import ReturnedCredit, ActualCredit
from fastapi import Depends, HTTPException
from database.db import get_session


def get_user_service(session: AsyncSession = Depends(get_session)) -> "UserService":
    return UserService(session)

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_user_credits(self, user_id: int):
        async with get_uow(self.session) as uow:
            user = await uow.user_repo.get_user_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            credits = await uow.credit_repo.get_user_credits(user_id)
            
            actual_credits = []
            returned_credits = []
            
            returned_credits = [
                ReturnedCredit.model_validate({
                    "issuance_date": credit.issuance_date,
                    "is_returned": True,
                    "act_return_date": credit.actual_return_date,
                    "body": credit.body,
                    "percents": credit.percent,
                    "payments": sum((payment.sum or 0) for payment in (credit.payments or []))
                })
                for credit in credits if credit.actual_return_date is not None
            ]
            

            
            today = date.today()
            for credit in credits:
                if credit.actual_return_date is None:
                    payments = credit.payments or []
                    body_payments = 0.0
                    percents_payments = 0.0
                    for p in payments:
                        if p.type_id == 'тіло':
                            body_payments += p.sum or 0
                        elif p.type_id == 'відсотки':
                            percents_payments += p.sum or 0

                    expired_days = 0
                    if credit.return_date and today > credit.return_date:
                        expired_days = (today - credit.return_date).days

                    actual_credits.append(
                        ActualCredit.model_validate(
                        {
                        "issuance_date": credit.issuance_date,
                        "is_returned": False,
                        "return_date": credit.return_date,
                        "expired_days": expired_days,
                        "body": credit.body,
                        "percents": credit.percent,
                        "body_payments": body_payments,
                        "percents_payments": percents_payments
                        }
                        ))
            
            return UserCredits(
                id=user.id,
                login=user.login,
                registration_date=user.registration_date,
                returned_credits=returned_credits,
                actual_credits=actual_credits
            )