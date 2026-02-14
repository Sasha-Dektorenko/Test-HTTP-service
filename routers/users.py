from fastapi import APIRouter, Depends
from services import UserService, get_user_service
from schemas import UserCredits

user_router = APIRouter(prefix="/user", tags=["users"])

@user_router.get("/credits/{user_id}", response_model=UserCredits)
async def get_user_credits(user_id: int, user_service: UserService = Depends(get_user_service)):
    return await user_service.get_user_credits(user_id)
    
    