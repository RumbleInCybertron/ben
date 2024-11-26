from fastapi import FastAPI
from app.database import Base, engine
from app.routes import router as user_router

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include user routes
app.include_router(user_router, prefix="/user", tags=["user"])

@app.get("/")
def root():
    return {"message": "User Authentication Service is running"}
