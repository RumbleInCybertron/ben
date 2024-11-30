from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.database import Base, engine
from app.routes import router as user_router
import logging

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)

@app.middleware("http")
async def log_request_data(request: Request, call_next):
    logging.debug(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logging.debug(f"Response status: {response.status_code}")
    return response


# Create database tables
Base.metadata.create_all(bind=engine)

# Include user routes
app.include_router(user_router, prefix="/user", tags=["Users"])

@app.get("/")
def root():
    return {"message": "User Authentication Service is running"}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred. Please try again later."}
    )
    
@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/debug")
def debug_routes():
    route_info = []
    for route in app.routes:
        route_info.append({
            "path": route.path,
            "name": route.name,
            "methods": list(route.methods or []),
        })
    return route_info
