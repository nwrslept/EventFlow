from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.models.event import Event
from app.schemas.event import EventCreate

async def create_event(db: AsyncSession, event: EventCreate, user_id: int):
    db_event = Event(
        **event.model_dump(),
        owner_id=user_id
    )
    db.add(db_event)
    await db.commit()
    await db.refresh(db_event)
    return db_event

async def get_user_events(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100):
    query = select(Event).filter(Event.owner_id == user_id).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def get_event(db: AsyncSession, event_id: int):
    query = select(Event).filter(Event.id == event_id)
    result = await db.execute(query)
    return result.scalars().first()


async def update_event(db: AsyncSession, db_event: Event, event_update: EventCreate):
    for key, value in event_update.model_dump().items():
        setattr(db_event, key, value)

    db.add(db_event)
    await db.commit()
    await db.refresh(db_event)
    return db_event


async def delete_event(db: AsyncSession, db_event: Event):
    await db.delete(db_event)
    await db.commit()