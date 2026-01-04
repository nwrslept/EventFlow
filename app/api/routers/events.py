from typing import List, Optional
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.event import EventCreate, EventResponse
from app.models.user import User
from app.api.deps import get_current_user
from app.crud import event as crud_event

router = APIRouter()

@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(
    event_in: EventCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await crud_event.create_event(db=db, event=event_in, user_id=current_user.id)

@router.get("/", response_model=List[EventResponse])
async def read_events(
    skip: int = 0,
    limit: int = 100,
    keyword: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return await crud_event.get_user_events(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        keyword=keyword
    )

@router.get("/{event_id}", response_model=EventResponse)
async def read_event(
        event_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    event = await crud_event.get_event(db, event_id=event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    return event


@router.put("/{event_id}", response_model=EventResponse)
async def update_event(
        event_id: int,
        event_in: EventCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    event = await crud_event.get_event(db, event_id=event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    if event.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this event")

    return await crud_event.update_event(db=db, db_event=event, event_update=event_in)


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
        event_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    event = await crud_event.get_event(db, event_id=event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    if event.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this event")

    await crud_event.delete_event(db=db, db_event=event)
    return None