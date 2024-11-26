from sqlalchemy import Column, Integer, String
from app.database import Base

class Reward(Base):
    __tablename__ = "rewards"

    reward_id = Column(Integer, primary_key=True, index=True)
    reward_name = Column(String(100), nullable=False)
    reward_item = Column(String(50), nullable=False)  # gold, diamond
    reward_qty = Column(Integer, nullable=False)