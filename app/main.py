from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routers import users, auth, events

app = FastAPI(title=settings.PROJECT_NAME)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/health")
async def health_check():
    return {"status": "ok"}

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, tags=["auth"])
app.include_router(events.router, prefix="/events", tags=["events"])