from fastapi import APIRouter, HTTPException
from app.services.processing_service import QuestProcessingService
from pydantic import BaseModel

class DailyLoginRequest(BaseModel):
    user_id: int

router = APIRouter()
processing_service = QuestProcessingService()

@router.post("/daily-login")
async def process_daily_login(request: DailyLoginRequest):
    response = await processing_service.process_daily_login(request.user_id)
    if not response:
        raise HTTPException(status_code=400, detail="Failed to update daily login")
    return response

@router.post("/")
async def create_user_quest(user_id: int, quest_id: int):
    response = await processing_service.process_daily_login(user_id, quest_id)
    if not response:
        raise HTTPException(status_code=400, detail="Failed to create user quest")
    return response

@router.put("/{user_id}/{quest_id}")
async def update_user_quest(user_id: int, quest_id: int):
    response = await processing_service.update_user_quest(user_id, quest_id)
    if not response:
        raise HTTPException(status_code=400, detail="Failed to update user quest")
    return response

@router.post("/sign-in-three-times")
async def process_sign_in_three_times(request: DailyLoginRequest):
    response = await processing_service.sign_in_three_times(request.user_id)
    if not response:
        raise HTTPException(status_code=400, detail="Failed to update sign in quest")
    return response