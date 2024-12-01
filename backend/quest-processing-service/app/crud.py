import requests
from sqlalchemy.orm import Session
from .models import UserQuestReward, QuestStatus
from datetime import datetime
import logging
import os

PORT = int(os.getenv("PORT", 8000))

USER_AUTH_URL = f"http://user-auth-service:{PORT}"
QUEST_CATALOG_URL = f"http://quest-catalog-service:{PORT}/catalog"

def validate_user(user_id: int):
    return True
    # try:
    #     logging.info(f"Fetching user from: {USER_AUTH_URL}/user/{user_id}")
    #     response = requests.get(f"{USER_AUTH_URL}/user/{user_id}")
    #     logging.info(f"Response: {response.status_code} - {response.text}")
    #     if response.status_code == 404:
    #         return False
    #     response.raise_for_status()
    #     return True
    # except Exception as e:
    #     print(f"Error validating user: {e}")
    #     return False

def validate_quest(quest_id: int):
    try:
        response = requests.get(f"{QUEST_CATALOG_URL}/quests/{quest_id}")
        response.raise_for_status()
        return True
    except Exception as e:
        logging.error(f"Error validating quest: {e}")
        return False

def create_user_quest_reward(db: Session, user_id: int, quest_id: int):
    if not validate_user(user_id):
        raise ValueError("User does not exist.")
    if not validate_quest(quest_id):
        raise ValueError("Quest does not exist.")
    
    new_reward = UserQuestReward(user_id=user_id, quest_id=quest_id, status="NOT_CLAIMED")
    db.add(new_reward)
    db.commit()
    db.refresh(new_reward)
    return new_reward

def update_quest_progress(db: Session, user_id: int, quest_id: int, progress: int):
    reward = db.query(UserQuestReward).filter(
        UserQuestReward.user_id == user_id,
        UserQuestReward.quest_id == quest_id
    ).first()

    if not reward:
        raise ValueError("User quest not found.")
    
    reward.progress = progress
    if progress == 100:
        reward.status = QuestStatus.CLAIMED
        reward.date_completed = datetime.utcnow()
    db.commit()
    db.refresh(reward)
    return reward

def complete_quest(db: Session, user_id: int, quest_id: int):
    reward = db.query(UserQuestReward).filter(
        UserQuestReward.user_id == user_id,
        UserQuestReward.quest_id == quest_id
    ).first()

    if not reward:
        raise ValueError("Quest not found for user")

    # Update quest status
    reward.status = "CLAIMED"
    db.commit()

    # Fetch quest details to determine reward
    quest_response = requests.get(f"http://quest-catalog-service:{PORT}/quests/{quest_id}")
    if quest_response.status_code != 200:
        raise ValueError("Quest details not found")
    quest_details = quest_response.json()

    # Award gold/diamonds (mock example)
    gold = 100
    diamond = 5 if "special" in quest_details["name"].lower() else 0

    # Call User Authentication Service to update rewards
    reward_response = requests.put(
        f"http://user-auth-service:{PORT}/user/{user_id}/reward",
        json={"gold": gold, "diamond": diamond}
    )

    if reward_response.status_code != 200:
        raise ValueError("Failed to update user rewards")
    return {"message": f"Quest {quest_id} completed for user {user_id}, rewards granted."}
