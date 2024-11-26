from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Reward, Quest, UserQuestReward
from pydantic import BaseModel, Field
from datetime import datetime

router = APIRouter()

# Pydantic schema for Quest
class QuestCreate(BaseModel):
    reward_id: int
    auto_claim: bool = False
    streak: int = 1
    duplication: int = 1
    name: str
    description: str

class QuestResponse(BaseModel):
    quest_id: int
    reward_id: int
    auto_claim: bool
    streak: int
    duplication: int
    name: str
    description: str

    class Config:
        orm_mode = True  # Allows Pydantic to work with SQLAlchemy models

# Pydantic schema for Reward
class RewardCreate(BaseModel):
    reward_name: str
    reward_item: str
    reward_qty: int
    
class RewardResponse(BaseModel):
    reward_id: int
    reward_name: str
    reward_item: str
    reward_qty: int

    class Config:
        orm_mode = True  # Allows Pydantic to work with SQLAlchemy models
        
# Pydantic schema for User Quest Rewards
class UserQuestRewardCreate(BaseModel):
    user_id: int
    quest_id: int
    status: str

class UserQuestRewardResponse(BaseModel):
    user_id: int
    quest_id: int
    status: str
    date: datetime

    class Config:
        orm_mode = True  # Allows Pydantic to work with SQLAlchemy models


## Quest routes        
@router.post("/quests/", response_model=dict)
def create_quest(quest: QuestCreate, db: Session = Depends(get_db)):
    # Validate reward_id exists
    reward = db.query(Reward).filter(Reward.reward_id == quest.reward_id).first()
    if not reward:
        raise HTTPException(status_code=404, detail="Reward not found")

    new_quest = Quest(**quest.dict())
    db.add(new_quest)
    db.commit()
    db.refresh(new_quest)
    return {"message": "Quest created successfully", "quest_id": new_quest.quest_id}

@router.get("/quests/", response_model=list[QuestResponse])
def list_quests(db: Session = Depends(get_db)):
    return db.query(Quest).all()

@router.get("/quests/{quest_id}", response_model=QuestResponse)
def get_quest(quest_id: int, db: Session = Depends(get_db)):
    quest = db.query(Quest).filter(Quest.quest_id == quest_id).first()
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")
    return quest

@router.put("/quests/{quest_id}", response_model=dict)
def update_quest(quest_id: int, quest: QuestCreate, db: Session = Depends(get_db)):
    db_quest = db.query(Quest).filter(Quest.quest_id == quest_id).first()
    if not db_quest:
        raise HTTPException(status_code=404, detail="Quest not found")

    for key, value in quest.dict().items():
        setattr(db_quest, key, value)
    db.commit()
    return {"message": "Quest updated successfully"}

@router.delete("/quests/{quest_id}", response_model=dict)
def delete_quest(quest_id: int, db: Session = Depends(get_db)):
    db_quest = db.query(Quest).filter(Quest.quest_id == quest_id).first()
    if not db_quest:
        raise HTTPException(status_code=404, detail="Quest not found")
    db.delete(db_quest)
    db.commit()
    return {"message": "Quest deleted successfully"}
        
## Reward routes
@router.post("/rewards/", response_model=dict)
def create_reward(reward: RewardCreate, db: Session = Depends(get_db)):
    new_reward = Reward(**reward.dict())
    db.add(new_reward)
    db.commit()
    db.refresh(new_reward)
    return {"message": "Reward created successfully", "reward_id": new_reward.reward_id}

@router.get("/rewards/", response_model=list[RewardResponse])
def list_rewards(db: Session = Depends(get_db)):
    return db.query(Reward).all()

@router.get("/rewards/{reward_id}", response_model=RewardResponse)
def get_reward(reward_id: int, db: Session = Depends(get_db)):
    reward = db.query(Reward).filter(Reward.reward_id == reward_id).first()
    if not reward:
        raise HTTPException(status_code=404, detail="Reward not found")
    return reward

@router.delete("/rewards/{reward_id}", response_model=dict)
def delete_reward(reward_id: int, db: Session = Depends(get_db)):
    reward = db.query(Reward).filter(Reward.reward_id == reward_id).first()
    if not reward:
        raise HTTPException(status_code=404, detail="Reward not found")
    db.delete(reward)
    db.commit()
    return {"message": "Reward deleted successfully"}


## User Quest Reward routes
@router.post("/user_quest_rewards/", response_model=dict)
def track_user_quest_reward(reward: UserQuestRewardCreate, db: Session = Depends(get_db)):
    # Validate quest_id exists
    quest = db.query(Quest).filter(Quest.quest_id == reward.quest_id).first()
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")

    # Check if the user quest reward already exists
    existing_reward = db.query(UserQuestReward).filter(
        UserQuestReward.user_id == reward.user_id,
        UserQuestReward.quest_id == reward.quest_id
    ).first()

    if existing_reward:
        # Update existing record
        existing_reward.status = reward.status
        existing_reward.date = func.now()
    else:
        # Create new record
        new_reward = UserQuestReward(**reward.dict())
        db.add(new_reward)

    db.commit()
    return {"message": "User quest reward tracked successfully"}

@router.get("/user_quest_rewards/{user_id}", response_model=list[UserQuestRewardResponse])
def get_user_quest_rewards(user_id: int, db: Session = Depends(get_db)):
    rewards = db.query(UserQuestReward).filter(UserQuestReward.user_id == user_id).all()
    if not rewards:
        raise HTTPException(status_code=404, detail="No rewards found for the user")
    return rewards
