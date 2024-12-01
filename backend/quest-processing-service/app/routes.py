from fastapi import APIRouter, Depends, HTTPException
import requests
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import UserQuestReward
from app.schemas import UserQuestProgress
from app.crud import create_user_quest_reward, update_quest_progress
from app.schemas import UserQuestRewardCreate, UserQuestRewardResponse
from datetime import datetime, timedelta
import os
import logging

PORT  = int(os.getenv("PORT", 8000))

router = APIRouter()

# Fetch base URLs from environment variables with default values
BASE_QUEST_CATALOG_URL = os.getenv("QUEST_CATALOG_URL", "http://quest-catalog-service")
BASE_USER_AUTH_URL = os.getenv("USER_AUTH_URL", "http://user-auth-service")
PORT = os.getenv("PORT", "8000")

# Construct the full URLs dynamically
QUEST_CATALOG_URL = f"{BASE_QUEST_CATALOG_URL}:{PORT}/catalog"
USER_AUTH_URL = f"{BASE_USER_AUTH_URL}:{PORT}/user"

@router.post("/daily-login", response_model=dict)
def process_daily_login(user_progress: UserQuestProgress, db: Session = Depends(get_db)):
    user_id = user_progress.user_id
    logging.info(f"Processing daily login for user_id: {user_id}")

    # Fetch quest details for "Daily Login"
    try:
        response = requests.get(f"{QUEST_CATALOG_URL}/quests")
        response.raise_for_status()
        quests = response.json()
        logging.info(f"Fetched quests: {quests}")
    except Exception as e:
        logging.error(f"Failed to fetch quests: {e}")
        raise HTTPException(status_code=500, detail="Unable to fetch quest details.")
    
    # Find daily login quest
    daily_login_quest = next((q for q in quests if q.get("name") == "Daily Login"), None)
    if not daily_login_quest:
        logging.error("Daily Login Quest not found.")
        raise HTTPException(status_code=404, detail="Daily Login Quest not found.")

    quest_id = daily_login_quest["quest_id"]
    required_streak = daily_login_quest["streak"]
    duplication = daily_login_quest["duplication"]
    reward_id = daily_login_quest["reward_id"]

    # Check progress
    user_quest = db.query(UserQuestReward).filter(
        UserQuestReward.user_id == user_id,
        UserQuestReward.quest_id == quest_id
    ).first()
    logging.info(f"User Quest: {user_quest}")

    now = datetime.utcnow()
    try:
        if user_quest:
            # Check duplication limit
            if user_quest.completion_count >= duplication:
                raise HTTPException(status_code=400, detail="Quest duplication limit reached.")

            # Update streak progress
            if user_quest.last_updated and (now - user_quest.last_updated).days == 1:
                user_quest.streak += 1
            else:
                user_quest.streak = 1 # resets streak if user misses a day

            # Check if streak requirement met
            if user_quest.streak >= required_streak:
                user_quest.status = "CLAIMED"
                user_quest.date_completed = now
            user_quest.completion_count += 1
            user_quest.last_updated = now
        else:
            # First time completing quest
            user_quest = UserQuestReward(
                user_id=user_id,
                quest_id=quest_id,
                streak=1,
                completion_count=1,
                last_updated=now,
                status="NOT_CLAIMED"
            )
            db.add(user_quest)

        db.commit()
        logging.info("User quest updated successfully.")
    except Exception as e:
        logging.error(f"Error updating user quest: {e}")
        raise HTTPException(status_code=500, detail="Error updating user quest.")

    # Fetch reward details
    try:
        reward_response = requests.get(f"{QUEST_CATALOG_URL}/rewards/{reward_id}")
        reward_response.raise_for_status()
        reward = reward_response.json()
        logging.info(f"Fetched reward details: {reward}")
    except Exception as e:
        logging.error(f"Failed to fetch reward details: {e}")
        raise HTTPException(status_code=500, detail="Unable to fetch reward details.")
        
    reward_item = reward["reward_item"]
    reward_qty = reward["reward_qty"]

    # Award user
    try:
        award_response = requests.put(
            f"{USER_AUTH_URL}/{user_id}/reward",
            json={reward_item: reward_qty}
        )
        logging.info(f"Reward Update Response: {award_response.status_code}, {award_response.text}")
        if award_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Unable to award the user.")
    except Exception as e:
        logging.error(f"Failed to award user: {e}")
        raise HTTPException(status_code=500, detail="Unable to award the user.")

    return {"message": "Daily Login Quest processed successfully."}

@router.post("/", response_model=UserQuestRewardResponse)
def create_user_quest(quest: UserQuestRewardCreate, db: Session = Depends(get_db)):
    try:
        return create_user_quest_reward(db, quest.user_id, quest.quest_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{user_id}/{quest_id}", response_model=UserQuestRewardResponse)
def update_user_quest(user_id: int, quest_id: int, progress: int, db: Session = Depends(get_db)):
    try:
        return update_quest_progress(db, user_id, quest_id, progress)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{user_id}/{quest_id}/claim", response_model=dict)
def claim_reward(user_id: int, quest_id: int, db: Session = Depends(get_db)):
    user_quest = db.query(UserQuestReward).filter(
        UserQuestReward.user_id == user_id,
        UserQuestReward.quest_id == quest_id,
        UserQuestReward.status == "NOT_CLAIMED"
    ).first()

    if not user_quest:
        raise HTTPException(status_code=404, detail="Quest not available for claiming.")

    # Fetch reward details from quest-catalog-service
    reward_response = requests.get(f"{QUEST_CATALOG_URL}/rewards/{quest_id}")
    if reward_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Unable to fetch reward details.")
    
    reward_details = reward_response.json()
    reward_item = reward_details["reward_item"]  # e.g., "gold" or "diamond"
    reward_qty = reward_details["reward_qty"]    # e.g., 100 or 5

    # Update user quest reward status to CLAIMED
    user_quest.status = "claimed"
    db.commit()

    # Notify user-auth-service to add rewards
    user_reward_update_response = requests.put(
        f"{USER_AUTH_URL}/{user_id}/reward",
        json={reward_item: reward_qty}
    )
    if user_reward_update_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Unable to award the user.")

    return {"message": "Reward claimed successfully."}

@router.post("/sign-in-three-times", response_model=dict)
def process_sign_in_three_times(user_progress: UserQuestProgress, db: Session = Depends(get_db)):
    user_id = user_progress.user_id
    logging.info(f"Processing Sign-In-Three-Times quest for user_id: {user_id}")

    # Fetch quest details for "Sign-In-Three-Times"
    try:
        response = requests.get(f"{QUEST_CATALOG_URL}/quests")
        response.raise_for_status()
        quests = response.json()
        logging.info(f"Fetched quests: {quests}")
    except Exception as e:
        logging.error(f"Failed to fetch quests: {e}")
        raise HTTPException(status_code=500, detail="Unable to fetch quest details.")
    
    # Find "Sign-In-Three-Times" quest
    try:
        quest = next((q for q in quests if q.get("name") == "Sign-In-Three-Times"), None)
        if not quest:
            raise HTTPException(status_code=404, detail="Sign-In-Three-Times Quest not found.")
    except Exception as e:
        logging.error(f"Error finding Sign-In-Three-Times quest: {e}")
        raise HTTPException(status_code=500, detail="Error processing quest data.")        

    quest_id = quest["quest_id"]
    required_streak = quest["streak"]
    duplication = quest["duplication"]
    reward_id = quest["reward_id"]

    # Check progress
    try:
        user_quest = db.query(UserQuestReward).filter(
            UserQuestReward.user_id == user_id,
            UserQuestReward.quest_id == quest_id
        ).first()
        logging.info(f"User Quest: {user_quest}")

        now = datetime.utcnow()
        if user_quest:
            # Check duplication limit
            if user_quest.completion_count >= duplication:
                raise HTTPException(status_code=400, detail="Quest duplication limit reached.")

            # Update streak progress
            if user_quest.last_updated and (now - user_quest.last_updated).days == 1:
                user_quest.streak += 1
            else:
                user_quest.streak = 1  # Reset streak if the user misses a day

            # Check if streak requirement met
            if user_quest.streak >= required_streak:
                user_quest.status = QuestStatus.NOT_CLAIMED  # Reward must be claimed manually
                user_quest.date_completed = now
            user_quest.completion_count += 1
            user_quest.last_updated = now
        else:
            # First time completing quest
            user_quest = UserQuestReward(
                user_id=user_id,
                quest_id=quest_id,
                streak=1,
                completion_count=1,
                last_updated=now,
                status=QuestStatus.NOT_CLAIMED
            )
            db.add(user_quest)

        db.commit()
        logging.info("User quest updated successfully.")
    except Exception as e:
        logging.error(f"Error updating user quest: {e}")
        raise HTTPException(status_code=500, detail="Error updating user quest.")    

    # Fetch reward details
    try:
        reward_response = requests.get(f"{QUEST_CATALOG_URL}/rewards/{reward_id}")
        reward_response.raise_for_status()
        reward = reward_response.json()
        logging.info(f"Fetched reward details: {reward}")
    except Exception as e:
        logging.error(f"Failed to fetch reward details: {e}")
        raise HTTPException(status_code=500, detail="Unable to fetch reward details.")    

    return {
        "message": "Sign-In-Three-Times Quest processed successfully.",
        "progress": {
            "streak": user_quest.streak,
            "completion_count": user_quest.completion_count,
            "status": user_quest.status,
        },
        "reward": {
            "reward_item": reward["reward_item"],
            "reward_qty": reward["reward_qty"],
        },
    }

@router.post("/initialize-user-quests", response_model=dict)
def initialize_user_quests(user_data: dict, db: Session = Depends(get_db)):
    user_id = user_data.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required.")

    try:
        # Fetch all quests from quest-catalog-service
        # ping endpoint
        requests.head(f"{QUEST_CATALOG_URL}/quests/")
        
        response = requests.get(f"{QUEST_CATALOG_URL}/quests/")
        response.raise_for_status()
        quests = response.json()

        # Create user_quest_rewards for each quest
        for quest in quests:
            user_quest = UserQuestReward(
                user_id=user_id,
                quest_id=quest["quest_id"],
                status="NOT_CLAIMED",
                progress=0,
                streak=0,
                completion_count=0,
                date_started=datetime.utcnow()
            )
            db.add(user_quest)

        db.commit()
        return {"message": "User quests initialized successfully."}
    except Exception as e:
        logging.error(f"Error initializing quests for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Error initializing user quests.")