from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.database import Base, engine
from app.routes import router as quest_router

# Create FastAPI app instance
app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include quest routes
app.include_router(quest_router, prefix="/user-quests", tags=["User Quests"])

@app.get("/")
def root():
    return {"message": "Quest Processing Service is running"}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred. Please try again later."}
    )
