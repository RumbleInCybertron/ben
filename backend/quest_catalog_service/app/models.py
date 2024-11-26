from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Quest(Base):
    __tablename__ = "quests"

    quest_id = Column(Integer, primary_key=True, index=True)
    reward_id = Column(Integer, ForeignKey("rewards.reward_id"))
    auto_claim = Column(Boolean, default=False)
    streak = Column(Integer, default=1)
    duplication = Column(Integer, default=1)
    name = Column(String(100), nullable=False)
    description = Column(Text)

    reward = relationship("Reward", back_populates="quests")

class Reward(Base):
    __tablename__ = "rewards"

    reward_id = Column(Integer, primary_key=True, index=True)
    reward_name = Column(String(100), nullable=False)
    reward_item = Column(String(50), nullable=False)  # gold, diamond
    reward_qty = Column(Integer, nullable=False)

    quests = relationship("Quest", back_populates="reward")