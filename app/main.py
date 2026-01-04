from fastapi import FastAPI
from app.core.config import settings
from app.api.routers import users

app = FastAPI(title=settings.PROJECT_NAME)

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "project": settings.PROJECT_NAME,
    }

app.include_router(users.router, prefix="/users", tags=["users"])