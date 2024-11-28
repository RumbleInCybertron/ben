from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.models import Quest, Reward
from app.database import Base, engine, SessionLocal
from app.routes import router as catalog_router

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include rewards routes
app.include_router(catalog_router, prefix="/catalog", tags=["catalog"])

@app.get("/")
def root():
    return {"message": "Quest Catalog Service is running"}

def populate_initial_data(db: Session):
    # Daily Login Quest and Reward
    daily_login_reward = db.query(Reward).filter_by(reward_name="Daily Login Reward").first()
    if not daily_login_reward:
        daily_login_reward = Reward(reward_name="Daily Login Reward", reward_item="gold", reward_qty=10)
        db.add(daily_login_reward)
        db.commit()
        db.refresh(daily_login_reward)

    daily_login_quest = db.query(Quest).filter_by(name="Daily Login").first()
    if not daily_login_quest:
        daily_login_quest = Quest(
            name="Daily Login",
            description="Log in daily to earn 10 gold.",
            reward_id=daily_login_reward.reward_id,
            auto_claim=True,
            streak=1,
            duplication=365
        )
        db.add(daily_login_quest)
        db.commit()
        
    # Sign In Three Times Quest and Reward
    sign_in_reward = db.query(Reward).filter_by(reward_name="Sign-In-Three-Times Reward").first()
    if not sign_in_reward:
        sign_in_reward = Reward(reward_name="Sign-In-Three-Times Reward", reward_item="diamond", reward_qty=10)
        db.add(sign_in_reward)
        db.commit()
        db.refresh(sign_in_reward)
        
    sign_in_quest = db.query(Quest).filter_by(name="Sign-In-Three-Times").first()
    if not sign_in_quest:
        sign_in_quest = Quest(
            name="Sign-In-Three-Times",
            description="Log in three times to earn diamonds.",
            reward_id=sign_in_reward.reward_id,
            auto_claim=False,
            streak=3,
            duplication=2
        )
        db.add(sign_in_quest)
        db.commit()

# Initialize the database with predefined data
db = SessionLocal()
populate_initial_data(db)
db.close()