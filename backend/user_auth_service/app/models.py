from sqlalchemy import Column, Integer, String, DateTime, func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    gold = Column(Integer, default=0)
    diamond = Column(Integer, default=0)
    status = Column(Integer, default=0)  # 0: new, 1: not_new, 2: banned
    created_at = Column(DateTime, default=func.now())
    last_login = Column(DateTime, default=None)
