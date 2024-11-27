from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base
from enum import Enum as PyEnum

# Enum for quest status
class QuestStatus(PyEnum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class UserQuestReward(Base):
    __tablename__ = "user_quest_rewards"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    quest_id = Column(Integer, nullable=False)
    status = Column(Enum(QuestStatus), default=QuestStatus.NEW, nullable=False)
    progress = Column(Integer, default=0)
    date_started = Column(DateTime, default=func.now())
    date_completed = Column(DateTime, nullable=True)
