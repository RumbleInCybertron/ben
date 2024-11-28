from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.database import get_db
from app.models import User
from app.auth import hash_password, verify_password, create_access_token
from app.exceptions import UserAlreadyExistsException, InvalidCredentialsException, DatabaseConnectionException
from pydantic import BaseModel
from app.schemas import UserResponse
from datetime import datetime, timedelta
from app.schemas import Token

router = APIRouter()

# Pydantic schemas
class UserCreate(BaseModel):
    user_name: str
    password: str

@router.post("/signup", response_model=dict)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    try:
        hashed_password = hash_password(user.password)
        new_user = User(user_name=user.user_name, password_hash=hashed_password)
        db.add(new_user)
        db.commit()
        return {"message": "User created successfully"}
    except SQLAlchemyError:
        db.rollback()
        raise UserAlreadyExistsException()

@router.post("/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # Fetch user from db
        db_user = db.query(User).filter(User.user_name == user.user_name).first()
        
        # Validate credentials
        if not db_user or not verify_password(user.password, db_user.password_hash):
            raise InvalidCredentialsException()
        
        # Handle login streak tracking
        now = datetime.utcnow()
        if db_user.last_login:
            delta = now - db_user.last_login
            if delta.days == 1:  # Consecutive login (1-day gap)
                db_user.gold += 10  # Award 10 gold for consecutive login
            elif delta.days > 1:
                # TODO Reset streak logic can be added here
                pass
        else:
            # First-time login handling (optional)
            db_user.gold += 5 

        # Update last login timestamp
        db_user.last_login = now
        db.commit()

        # Create access token
        access_token = create_access_token(data={"sub": db_user.user_name})
        return {
            "access_token": access_token, 
            "token_type": "bearer",
            "gold": db_user.gold,
            "diamond": db_user.diamond,
        }
    except InvalidCredentialsException:
        raise
    except SQLAlchemyError:
        raise DatabaseConnectionException()
    
@router.get("/users/")
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"id": user.user_id, "username": user.user_name} for user in users]

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    print(f"Fetching user with user_id: {user_id}")  # Debug log
    user = db.query(User).filter(User.user_id == user_id).first()
    print(f"User fetched: {user}")  # Debug log
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}/reward", response_model=dict)
def update_user_rewards(user_id: int, rewards: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update user attributes dynamically based on rewards
    for reward_item, reward_qty in rewards.items():
        if hasattr(user, reward_item):
            setattr(user, reward_item, getattr(user, reward_item) + reward_qty)
        else:
            raise HTTPException(status_code=400, detail=f"Invalid reward item: {reward_item}")

    db.commit()
    return {"message": "User rewards updated successfully."}

# @router.get("/debug")
# def debug_route():
#     raise ValueError("This is a test for the global exception handler")
