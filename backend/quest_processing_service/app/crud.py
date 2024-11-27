import requests
from sqlalchemy.orm import Session
from .models import UserQuestReward, QuestStatus
from datetime import datetime

def validate_user(user_id: int) -> bool:
    response = requests.get(f"http://user_auth_service:8001/user/{user_id}")
    return response.status_code == 200

def validate_quest(quest_id: int) -> bool:
    response = requests.get(f"http://quest_catalog_service:8002/quests/{quest_id}")
    return response.status_code == 200

def create_user_quest_reward(db: Session, user_id: int, quest_id: int):
    if not validate_user(user_id):
        raise ValueError("User does not exist.")
    if not validate_quest(quest_id):
        raise ValueError("Quest does not exist.")
    
    new_reward = UserQuestReward(user_id=user_id, quest_id=quest_id)
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
        reward.status = QuestStatus.COMPLETED
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
    reward.status = "completed"
    db.commit()

    # Fetch quest details to determine reward
    quest_response = requests.get(f"http://quest_catalog_service:8002/quests/{quest_id}")
    if quest_response.status_code != 200:
        raise ValueError("Quest details not found")
    quest_details = quest_response.json()

    # Award gold/diamonds (mock example)
    gold = 100
    diamond = 5 if "special" in quest_details["name"].lower() else 0

    # Call User Authentication Service to update rewards
    reward_response = requests.put(
        f"http://user_auth_service:8001/user/{user_id}/reward",
        json={"gold": gold, "diamond": diamond}
    )

    if reward_response.status_code != 200:
        raise ValueError("Failed to update user rewards")
    return {"message": f"Quest {quest_id} completed for user {user_id}, rewards granted."}
