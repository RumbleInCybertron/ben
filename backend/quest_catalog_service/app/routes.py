from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Reward
from pydantic import BaseModel

router = APIRouter()

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
