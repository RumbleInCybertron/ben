from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
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

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred. Please try again later."}
    )