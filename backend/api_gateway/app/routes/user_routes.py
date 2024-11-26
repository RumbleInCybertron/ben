from fastapi import APIRouter, HTTPException, Depends
from app.services.user_service import UserAuthService

router = APIRouter()
user_service = UserAuthService()

@router.post("/signup")
async def signup(user_data: dict):
    response = await user_service.signup(user_data)
    if not response:
        raise HTTPException(status_code=400, detail="Signup failed")
    return response

@router.post("/login")
async def login(user_data: dict):
    response = await user_service.login(user_data)
    if not response:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return response
