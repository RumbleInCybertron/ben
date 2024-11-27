from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import create_user_quest_reward, update_quest_progress
from app.schemas import UserQuestRewardCreate, UserQuestRewardResponse

router = APIRouter()

@router.post("/", response_model=UserQuestRewardResponse)
def create_user_quest(quest: UserQuestRewardCreate, db: Session = Depends(get_db)):
    try:
        return create_user_quest_reward(db, quest.user_id, quest.quest_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{user_id}/{quest_id}", response_model=UserQuestRewardResponse)
def update_user_quest(user_id: int, quest_id: int, progress: int, db: Session = Depends(get_db)):
    try:
        return update_quest_progress(db, user_id, quest_id, progress)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
