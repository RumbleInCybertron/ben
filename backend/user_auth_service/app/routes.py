from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.database import get_db
from app.models import User
from app.auth import hash_password, verify_password, create_access_token
from app.exceptions import UserAlreadyExistsException, InvalidCredentialsException, DatabaseConnectionException
from pydantic import BaseModel

router = APIRouter()

# Pydantic schemas
class UserCreate(BaseModel):
    user_name: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

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

        # Create access token
        access_token = create_access_token(data={"sub": db_user.user_name})
        return {"access_token": access_token, "token_type": "bearer"}
    except InvalidCredentialsException:
        raise
    except SQLAlchemyError:
        raise DatabaseConnectionException()

# @router.get("/debug")
# def debug_route():
#     raise ValueError("This is a test for the global exception handler")
