from fastapi import FastAPI
from app.database import Base, engine
from app.routes import router as rewards_router

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include rewards routes
app.include_router(rewards_router, prefix="/catalog", tags=["rewards"])

@app.get("/")
def root():
    return {"message": "Quest Catalog Service is running"}
