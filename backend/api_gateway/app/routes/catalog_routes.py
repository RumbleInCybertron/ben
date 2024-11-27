from fastapi import APIRouter, HTTPException
from app.services.catalog_service import QuestCatalogService

router = APIRouter()
catalog_service = QuestCatalogService()

@router.get("/quests/")
async def list_quests():
    try:
        quests = await catalog_service.list_quests()
        if not quests:
            raise HTTPException(status_code=404, detail="No quests found")
        return quests
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch quests: {str(e)}")

## TODO Update all routes with better Exception handling SEE above  
@router.get("/quests/{quest_id}")
async def get_quest(quest_id: int):
    response = await catalog_service.get_quest(quest_id)
    if not response:
        raise HTTPException(status_code=404, detail="Quest not found")
    return response

@router.post("/quests/")
async def create_quest(data: dict):
    response = await catalog_service.create_quest(data)
    if not response:
        raise HTTPException(status_code=400, detail="Failed to create quest")
    return response

@router.put("/quests/{quest_id}")
async def update_quest(quest_id: int, data: dict):
    response = await catalog_service.update_quest(quest_id, data)
    if not response:
        raise HTTPException(status_code=400, detail="Failed to update quest")
    return response

@router.delete("/quests/{quest_id}")
async def delete_quest(quest_id: int):
    response = await catalog_service.delete_quest(quest_id)
    if not response:
        raise HTTPException(status_code=400, detail="Failed to delete quest")
    return response
  
@router.get("/rewards/")
async def list_rewards():
    response = await catalog_service.list_rewards()
    if not response:
        raise HTTPException(status_code=404, detail="No rewards found")
    return response

@router.get("/rewards/{reward_id}")
async def get_reward(reward_id: int):
    response = await catalog_service.get_reward(reward_id)
    if not response:
        raise HTTPException(status_code=404, detail="Reward not found")
    return response

@router.post("/rewards/")
async def create_reward(data: dict):
    response = await catalog_service.create_reward(data)
    if not response:
        raise HTTPException(status_code=400, detail="Failed to create reward")
    return response

@router.delete("/rewards/{reward_id}")
async def delete_reward(reward_id: int):
    response = await catalog_service.delete_reward(reward_id)
    if not response:
        raise HTTPException(status_code=400, detail="Failed to delete reward")
    return response

@router.post("/user_quest_rewards/")
async def track_user_quest_rewards(data: dict):
    response = await catalog_service.track_user_quest_rewards(data)
    if not response:
        raise HTTPException(status_code=400, detail="Failed to track user quest reward")
    return response

@router.get("/user_quest_rewards/{user_id}")
async def get_user_quest_rewards(user_id: int):
    response = await catalog_service.get_user_quest_rewards(user_id)
    if not response:
        raise HTTPException(status_code=404, detail="User quest rewards not found")
    return response