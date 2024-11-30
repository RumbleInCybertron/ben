from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class QuestStatus(str, Enum):
    CLAIMED = "CLAIMED"
    NOT_CLAIMED = "NOT_CLAIMED"

class UserQuestRewardCreate(BaseModel):
    user_id: int
    quest_id: int

class UserQuestRewardResponse(BaseModel):
    id: int
    user_id: int
    quest_id: int
    status: QuestStatus
    progress: int
    streak: int
    completion_count: int
    date_started: datetime
    last_updated: Optional[datetime]
    date_completed: Optional[datetime]

    class Config:
        orm_mode = True

class UserQuestProgress(BaseModel):
    user_id: int