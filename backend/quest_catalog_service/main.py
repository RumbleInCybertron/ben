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
    # Check if the reward exists
    reward = db.query(Reward).filter_by(reward_name="Daily Login Reward").first()
    if not reward:
        reward = Reward(reward_name="Daily Login Reward", reward_item="gold", reward_qty=10)
        db.add(reward)
        db.commit()
        db.refresh(reward)

    # Check if the daily login quest exists
    quest = db.query(Quest).filter_by(name="Daily Login").first()
    if not quest:
        quest = Quest(
            name="Daily Login",
            description="Log in daily to earn 10 gold.",
            reward_id=reward.reward_id,
            auto_claim=True,
            streak=1,
            duplication=365
        )
        db.add(quest)
        db.commit()

# Initialize the database with predefined data
db = SessionLocal()
populate_initial_data(db)
db.close()