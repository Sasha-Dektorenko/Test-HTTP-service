from fastapi import APIRouter, Depends
from services import PlansService, get_plans_service
from fastapi import UploadFile, File


plan_router = APIRouter(prefix="/plans", tags=["plans"])

@plan_router.post("/insert")
async def insert_plans(file: UploadFile = File(...), plans_service: PlansService = Depends(get_plans_service)):
    return await plans_service.insert_plans(file)

