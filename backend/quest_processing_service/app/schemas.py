from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class QuestStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class UserQuestRewardCreate(BaseModel):
    user_id: int
    quest_id: int

class UserQuestRewardResponse(BaseModel):
    id: int
    user_id: int
    quest_id: int
    status: QuestStatus
    progress: int
    date_started: datetime
    date_completed: Optional[datetime]

    class Config:
        orm_mode = True
