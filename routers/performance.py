from fastapi import APIRouter, Depends
from services import PlansService, get_plans_service
from fastapi import UploadFile, File
from schemas.plans import PlanPerformance_3, PlanPerformance_4
from datetime import date


performance_router = APIRouter(prefix="/performance", tags=["performance"])


@performance_router.get("/plans", response_model=list[PlanPerformance_4 | PlanPerformance_3])
async def plans_performance(date: date, plans_service: PlansService = Depends(get_plans_service)):
    return await plans_service.plans_performance(date)
