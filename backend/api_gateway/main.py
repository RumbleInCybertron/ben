from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.routes import user_routes, catalog_routes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(user_routes.router, prefix="/user", tags=["User Authentication"])
app.include_router(catalog_routes.router, prefix="/catalog", tags=["Quest Catalog"])

@app.get("/")
def root():
    return {"message": "API Gateway is running"}
