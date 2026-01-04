from fastapi import FastAPI
from app.core.config import settings
from app.api.routers import users, auth, events

app = FastAPI(title=settings.PROJECT_NAME)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, tags=["auth"])
app.include_router(events.router, prefix="/events", tags=["events"])